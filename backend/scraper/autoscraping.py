import scraper.scraper as sc
import database.db_manager as db
from datetime import datetime


def auto_scraping():
    """
    Run every 5 minutes to get dynamic station data and weather data.
    """
    # get dynamic station data and current weather data:
    bikes = sc.get_bike_data()
    if bikes:
        db.write_to_db_station(bikes)
        db.write_to_db_avail(bikes)
    current_weather = sc.get_current_weather()
    if current_weather:
        db.write_to_db_current_weather(current_weather)
    now = datetime.now()
    if 0 <= now.minute < 10:
        forecast_hourly = sc.get_hourly_weather()
        if forecast_hourly:
            db.write_to_db_forecast_hourly(forecast_hourly)
    if now.hour == 0 and 0 <= now.minute < 10:
        forecast_daily = sc.get_daily_weather()
        if forecast_daily:
            db.write_to_db_forecast_daily(forecast_daily)


if __name__ == "__main__":
    auto_scraping()
