import os
from garminconnect import Garmin
from dotenv import load_dotenv
from influxdb import InfluxDBClient
from datetime import datetime
load_dotenv()

garmin_email = os.getenv("GARMIN_EMAIL")
garmin_password = os.getenv("GARMIN_PASSWORD")
influx_host = os.getenv("INFLUX_HOST")
influx_port = int(os.getenv("INFLUX_PORT", "8086"))
influx_user = os.getenv("INFLUX_USER")
influx_pass = os.getenv("INFLUX_PASS")
influx_db = os.getenv("INFLUX_DB")

def get_garmin_client(garmin_email=None, garmin_password=None):
    if garmin_email is None:
        garmin_email = os.getenv("GARMIN_EMAIL")
    if garmin_password is None:
        garmin_password = os.getenv("GARMIN_PASSWORD")
    garmin_client = Garmin(garmin_email, garmin_password)
    garmin_client.login()
    return garmin_client

def get_influx_client():
    influx_client = InfluxDBClient(
        host=influx_host,
        port=influx_port,
        username=influx_user,
        password=influx_pass,
        database=influx_db
    )
    return influx_client
