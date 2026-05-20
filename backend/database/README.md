# Statement about database functions
## db_setup.py

### Statement about version:
As sqlalchemy has been updated, the syntax is different from the code in the slide. 
To run the functions, please update sqlalchemy to the newest version using: pip install --upgrade sqlalchemy

### Statement about functions:
##### create_db_engine(): to create database and return the engine.
##### create_tables(): to create tables in the database.
### 
##### This file creates a database engine after setting up the tables, which can be imported and used by other modules.

## db_manager

### Statement about functions:
##### write_to_db_station(stations): write the static data of station to database.
##### write_to_db_avail(stations): write the dynamic data of station to database.
##### write_to_db_current_weather(weather): write the data of current weather to database.
##### write_to_db_forecast_hourly(weathers): write the forecast data of weather to database.
##### write_to_db_forecast_daily(weathers): write the forecast data of weather to database.

##### read_stations():Return the list of stations with their static data.
##### read_station_history(station_number):Return the historical data of last 24 hours of the single selected station.
##### read_daily_average(station_number):Return the historical data of last 7 days of a single selected station.
##### read_current_weather(): Return the newest current weather.
##### read_forecast_hourly(): Return the list of the hourly forecast weather data.
##### read_forecast_daily(): Return the list of the daily forecast weather data.

##### create_user(userdata:dict): Write user data to database when creating user account. Return 1 if succeeds. Return -1 if email already exsists. Return 0 if fails of other errors.
##### update_user_data(userdata:dict): return 1 if succeeds. Return -1 if email already exsists.  Return 0 if fails of other errors.
##### write_to_db_favorate(uid,station_number): Write user data station to database when saving station. return 1 if succeeds else 0. 
##### read_user_security(username):Return the password and token of a specific user.
##### read_user_data(uid): Read user data from database including favorate stations.

##### find_nearest(lat,lng): return the nearest station to the given location with availeble bikes.

##### other functions not listed here are called internally.
