import json
from datetime import datetime
from http.client import HTTPConnection


HOST = "127.0.0.1"
PORT = 8000


def _post_json(path, payload):
    # Send a single JSON POST request and return status, reason, and body
    body = json.dumps(payload).encode("utf-8")
    conn = HTTPConnection(HOST, PORT, timeout=10)
    conn.request(
        "POST",
        path,
        body=body,
        headers={"Content-Type": "application/json", "Content-Length": str(len(body))},
    )
    response = conn.getresponse()
    data = response.read().decode("utf-8", errors="replace")
    conn.close()
    return response.status, response.reason, data


def _try_parse_json(body_text):
    # Best-effort JSON detection to avoid parsing non-JSON responses
    stripped = body_text.strip()
    if not stripped:
        return None
    if not ((stripped.startswith("{") and stripped.endswith("}")) or (stripped.startswith("[") and stripped.endswith("]"))):
        return None
    return json.loads(stripped)


def main():
    # Hardcoded defaults (no CLI parsing)
    args = {
        "host": HOST,
        "port": PORT,
        "username": "demo",
        "email": "demo@example.com",
        "password_hash": "demo_hash",
        "user_id": 1,
        "location": "48.2738,-1.858",
        "refresh_rate": 45,
        "skip_create": False,
        "skip_weather": False,
        "skip_settings": False,
    }
    global HOST, PORT
    HOST = args["host"]
    PORT = args["port"]

    user_id = args["user_id"]

    if not args["skip_create"]:
        # Create the user and capture the assigned user_id if returned
        status, reason, body = _post_json(
            "/auth",
            {
                "action": "create_user",
                "username": args["username"],
                "email": args["email"],
                "password_hash": args["password_hash"],
            },
        )
        print("create_user:", status, reason)
        print(body)
        parsed = _try_parse_json(body)
        if parsed and isinstance(parsed, dict):
            user = parsed.get("user", {})
            if isinstance(user, dict) and user.get("user_id"):
                user_id = user["user_id"]

    if not args["skip_weather"]:
        # Trigger weather update for the user
        status, reason, body = _post_json(
            "/auth",
            {
                "action": "update_weather",
                "user_id": user_id,
                "password_hash": args["password_hash"],
                "location": args["location"],
                "timestamp": datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p"),
            },
        )
        print("\nupdate_weather:", status, reason)
        print(body)

    if not args["skip_settings"]:
        # Update user settings such as location and refresh rate
        status, reason, body = _post_json(
            "/auth",
            {
                "action": "update_settings",
                "user_id": user_id,
                "password_hash": args["password_hash"],
                "location": args["location"],
                "refreshRate_minutes": args["refresh_rate"],
            },
        )
        print("\nupdate_settings:", status, reason)
        print(body)


if __name__ == "__main__":
    main()
