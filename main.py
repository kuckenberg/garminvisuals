import os
from garminconnect import Garmin
from dotenv import load_dotenv
from influxdb import InfluxDBClient
from datetime import datetime
load_dotenv()

email = os.getenv("GARMIN_EMAIL")
password = os.getenv("GARMIN_PASSWORD")
influx_host = os.getenv("INFLUX_HOST")
influx_port = int(os.getenv("INFLUX_PORT", "8086"))
influx_user = os.getenv("INFLUX_USER")
influx_pass = os.getenv("INFLUX_PASS")
influx_db = os.getenv("INFLUX_DB")
influx_measurement = os.getenv("INFLUX_MEASUREMENT", "garminactivities")


def get_garmin_client(garmin_email, garmin_password):
    garmin_client = Garmin(garmin_email, garmin_password)
    garmin_client.login()
    return garmin_client


def get_last_activity(garmin_client):
    last_activity = garmin_client.get_activities(0, 1)[0]
    return last_activity


def get_influx_client():
    influx_client = InfluxDBClient(
        host=influx_host,
        port=influx_port,
        username=influx_user,
        password=influx_pass,
        database=influx_db
    )
    return influx_client

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

def main():
    garmin_client = get_garmin_client(email, password)
    influx_client = get_influx_client()
    last_activity = get_last_activity(garmin_client)
    write_activity_to_influx(last_activity, influx_client)

if __name__ == "__main__":
    main()









