import scraper.scraper as sc
import database.db_manager as db

def first_scraping():
    '''
    Run once to create database,tables and static station information. 
    '''
    # get and write static data of the stations and other original data
    bikes=sc.get_bike_data()
    if bikes:
        db.write_to_db_station(bikes)
        db.write_to_db_avail(bikes)
    current_weather=sc.get_current_weather()
    if current_weather:
        db.write_to_db_current_weather(current_weather)
    forecast_hourly=sc.get_hourly_weather()
    if forecast_hourly:
        db.write_to_db_forecast_hourly(forecast_hourly)    
    forecast_daily=sc.get_daily_weather()
    if forecast_daily:
        db.write_to_db_forecast_daily(forecast_daily)

if __name__=="__main__":
    first_scraping()