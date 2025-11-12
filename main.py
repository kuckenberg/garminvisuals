import argparse
from garmin_utils import get_garmin_client, get_influx_client
from fetch_last_activity import get_last_activity, write_activity_to_influx
from fetch_daily_stats import fetch_and_store_daily_stats

def main():
    parser = argparse.ArgumentParser(description="Garmin Datenabruf und Speicherung")
    parser.add_argument("job", choices=["last_activity", "daily_stats"], help="Welcher Job soll ausgeführt werden?")
    parser.add_argument("--date", type=str, default=None, help="Datum im Format YYYY-MM-DD (optional, nur für daily_stats)")
    args = parser.parse_args()

    if args.job == "last_activity":
        garmin_client = get_garmin_client()
        influx_client = get_influx_client()
        last_activity = get_last_activity(garmin_client)
        write_activity_to_influx(last_activity, influx_client)
    elif args.job == "daily_stats":
        garmin_client = get_garmin_client()
        influx_client = get_influx_client()
        fetch_and_store_daily_stats(garmin_client, influx_client, date_str=args.date)

if __name__ == "__main__":
    main()