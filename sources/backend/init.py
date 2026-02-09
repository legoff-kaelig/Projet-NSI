import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from API.weather_data import update_weather_for_user
from user_manager import UserManager
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8000


def _read_json_body(handler):
    content_length = handler.headers.get("Content-Length", "0")
    length = int(content_length) if content_length.isdigit() else 0

    raw_body = handler.rfile.read(length)
    body_text = raw_body.decode("utf-8", errors="replace")
    if not body_text:
        return {}
    try:
        return json.loads(body_text)
    except json.JSONDecodeError:
        return None


def _send_json(handler, status, payload):
    try:
        body = json.dumps(payload).encode("utf-8")

        handler.send_response(status)
        handler.send_header("Content-Type", "application/json")
        handler.send_header("Content-Length", str(len(body)))

        handler.send_header("Access-Control-Allow-Origin", "*")
        handler.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        handler.send_header("Access-Control-Allow-Headers", "Content-Type")

        handler.end_headers()
        handler.wfile.write(body)

    except (ConnectionAbortedError, BrokenPipeError):
        print("⚠️ Client disconnected before response was sent")


def _parse_location(data):
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    location = data.get("location")
    if location and (latitude is None or longitude is None):
        try:
            lat_text, lon_text = location.split(",", 1)
            latitude = float(lat_text.strip())
            longitude = float(lon_text.strip())
        except ValueError:
            return None, None

    return latitude, longitude


def _user_payload(user):
    return {
        "user_id": user[0],
        "username": user[1],
        "email": user[2],
        "location": user[4],
        "is24HourFormat": user[5],
        "isMetricSystem": user[6],
        "setupWizardDone": user[7],
        "refreshRate_minutes": user[8],
        "city": user[9],
    }


class AuthRequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path != "/auth":
            _send_json(self, 404, {"status": "error", "message": "Not found"})
            return

        data = _read_json_body(self)
        if data is None:
            _send_json(self, 400, {"status": "error", "message": "Invalid JSON"})
            return

        action = data.get("action")
        if action not in {"create_user", "update_settings", "update_weather"}:
            _send_json(
                self,
                400,
                {"status": "error", "message": "Unknown action"},
            )
            return

        if action == "create_user":
            username = data.get("username")
            email = data.get("email")
            password_hash = data.get("password_hash")
            with UserManager() as manager:
                new_user_id = manager.create_user(username, email, password_hash)
            if not new_user_id:
                _send_json(
                    self,
                    409,
                    {"status": "error", "message": "User already exists"},
                )
                return

            with UserManager() as manager:
                user = manager.get_user(new_user_id)
            _send_json(
                self,
                201,
                {
                    "status": "ok",
                    "message": "User created",
                    "action": action,
                    "user": _user_payload(user),
                },
            )
            return

        user_id = data.get("user_id")
        password_hash = data.get("password_hash")
        with UserManager() as manager:
            user = manager.get_user(user_id)
        if not user:
            _send_json(
                self,
                404,
                {"status": "error", "message": "User not found"},
            )
            return

        stored_hash = user[3]
        if stored_hash != password_hash:
            _send_json(
                self,
                401,
                {"status": "error", "message": "Invalid credentials"},
            )
            return

        if action == "update_settings":
            updates = {
                "username": data.get("username"),
                "email": data.get("email"),
                "location": data.get("location"),
                "city": data.get("city"),
                "is24HourFormat": data.get("is24HourFormat"),
                "isMetricSystem": data.get("isMetricSystem"),
                "setupWizardDone": data.get("setupWizardDone"),
                "refreshRate_minutes": data.get("refreshRate_minutes"),
            }
            filtered_updates = {}
            for key, value in updates.items():
                if value is not None:
                    filtered_updates[key] = value
            updates = filtered_updates
            if not updates:
                _send_json(
                    self,
                    400,
                    {"status": "error", "message": "No settings to update"},
                )
                return

            with UserManager() as manager:
                updated = manager.update_user(user_id, **updates)
            if not updated:
                _send_json(
                    self,
                    400,
                    {"status": "error", "message": "Update failed"},
                )
                return

            with UserManager() as manager:
                user = manager.get_user(user_id)
            _send_json(
                self,
                200,
                {
                    "status": "ok",
                    "message": "Settings updated",
                    "action": action,
                    "user": _user_payload(user),
                },
            )
            return

        timestamp = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
        latitude, longitude = _parse_location(data)
        if latitude is None or longitude is None:
            _send_json(
                self,
                400,
                {"status": "error", "message": "Missing location"},
            )
            return

        ok, info = update_weather_for_user(
            user_id=user_id,
            latitude=latitude,
            longitude=longitude,
            timestamp=timestamp,
        )
        if not ok:
            status_code = 502
            if isinstance(info, str):
                if info == "User not found":
                    status_code = 404
                elif info.startswith("Refresh not ready"):
                    status_code = 429
            _send_json(
                self,
                status_code,
                {
                    "status": "error",
                    "message": "Weather update failed",
                    "details": info,
                },
            )
            return

        with UserManager() as manager:
            user = manager.get_user(user_id)
        _send_json(
            self,
            200,
            {
                "status": "ok",
                "message": "Weather updated",
                "action": action,
                "user": _user_payload(user),
                "weather_update": info,
            },
        )

def run():
    server = HTTPServer((HOST, PORT), AuthRequestHandler)
    print(f"Auth server listening on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()