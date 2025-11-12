from garmin_utils import get_garmin_client, get_influx_client
from dotenv import load_dotenv
import os

load_dotenv()

influx_measurement = os.getenv("INFLUX_MEASUREMENT", "garminactivities")


def get_last_activity(garmin_client):
    last_activity = garmin_client.get_activities(0, 1)[0]
    return last_activity


def check_activity_exists(activity_id, influx_client):
        query = f"SELECT * FROM {influx_measurement} WHERE activityId = '{activity_id}' LIMIT 1"
        result = influx_client.query(query)
        return any(result.get_points())


def write_activity_to_influx(last_activity, influx_client):
    if check_activity_exists(last_activity["activityId"], influx_client):
        print("Activity already exists in InfluxDB")
        return
    json_body = [{
        "measurement": influx_measurement,
        "tags": {
            "location": last_activity.get("locationName", "unknown"),
            "activityType": last_activity.get("activityType", "unknown")
        },
        "fields": {
            "activityId": str(last_activity["activityId"]),
            "distance": float(last_activity.get("distance", 0)),
            "duration": float(last_activity.get("duration", 0))
        },
        "time": last_activity.get("startTimeLocal")
    }]
    influx_client.write_points(json_body)
    print("Activity written to InfluxDB!")









