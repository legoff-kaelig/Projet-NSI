import os
import sqlite3

class ReverseGeocoding:
    """Reverse-geocoding a latitude/longitude pair using a SQLite DB."""

    def __init__(self, lat: str, lon: str, db_path: str = "villes_france.sqlite", table_name: str = "villes_france_free"):
        # Normalize inputs to avoid whitespace mismatches in SQL LIKE queries
        self.lat = lat.strip()
        self.lon = lon.strip()
        self.table_name = table_name

        if not os.path.isabs(db_path):
            base_dir = os.path.dirname(__file__)
            db_path = os.path.join(base_dir, db_path)

        # Connects the DB and sets a cursor
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()

    def _query_best(self, lat_prefix: str, lon_prefix: str) -> str | None:
        """Returns the name of the closest matching city based on latitude and longitude prefixes, or None if no match is found"""
        request = f"""
            SELECT ville_nom
            FROM (
                SELECT
                    ville_nom,
                    ville_latitude_deg,
                    ville_longitude_deg
                FROM {self.table_name}
                WHERE ville_latitude_deg LIKE '{lat_prefix}%' AND ville_longitude_deg LIKE '{lon_prefix}%'
            )
            ORDER BY ABS(ville_latitude_deg - {self.lat}) + ABS(ville_longitude_deg - {self.lon})
            LIMIT 1
        """
        self.cur.execute(request)
        row = self.cur.fetchone()
        return row[0] if row else None

    def find_city(self) -> str | None:
        """Return the first matching city name, or None if nothing is found."""
        # Gradually shorten prefixes until a match is found
        max_trim = min(len(self.lat), len(self.lon))
        for step in range(0, max_trim):
            if step > 0:
                lat_prefix = self.lat[:-step]
                lon_prefix = self.lon[:-step]
            else:
                lat_prefix = self.lat
                lon_prefix = self.lon

            city = self._query_best(lat_prefix, lon_prefix)
            if city is not None:
                return city

        return None
    
    def close_connection(self):
        """Close the database connection."""
        # Cleanup for caller convenience
        if self.con is not None:
            self.con.close()
            self.con = None
            self.cur = None


def _test():
    """Basic runtime test for a known coordinate pair"""
    latitude = "48.2738000"
    longitude = "-1.8580000"

    request = ReverseGeocoding(latitude, longitude)
    city = request.find_city()
    assert city is not None
    request.close_connection()

if __name__ == "__main__":
    if os.path.exists(os.path.join(os.path.dirname(__file__), "villes_france.sqlite")):
        _test()
