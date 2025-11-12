from garmin_utils import get_garmin_client, get_influx_client
from datetime import datetime, timedelta

def safe_int(val):
    try:
        return int(val)
    except (TypeError, ValueError):
        return 0

def safe_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0


def fetch_and_store_daily_stats(garmin_client, influx_client, date_str=None):
    # Erlaube explizites Datum, sonst heute
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    stats = garmin_client.get_stats(date_str)
    print(f"Stats-Rohdaten für {date_str}:", stats)
    # Vorherigen Eintrag für diesen Tag löschen (InfluxDB 1.x)
    delete_query = f"DELETE FROM garmindailystats WHERE date = '{date_str}'"
    influx_client.query(delete_query)
    # Felder schreiben
    json_body = [{
        "measurement": "garmindailystats",
        "tags": {
            "date": date_str
        },
        "fields": {
            "steps": safe_int(stats.get("totalSteps")),
            "calories": safe_int(stats.get("totalKilocalories")),
            "distance": safe_float(stats.get("totalDistanceMeters")),
            "floorsClimbed": safe_int(stats.get("floorsClimbed")),
            "activeMinutes": safe_int(stats.get("moderateIntensityMinutes")),
        },
        "time": date_str + "T00:00:00Z"
    }]
    influx_client.write_points(json_body)
    print(f"Tagesstatistiken für {date_str} gespeichert:", json_body)