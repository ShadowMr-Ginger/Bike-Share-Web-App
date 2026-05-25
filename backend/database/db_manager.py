# 1. --- Imports ---

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from database.db_setup import engine
import json
import requests
from datetime import datetime, timedelta
import uuid
import hashlib


# --------------------- Functions for writing data to database--------------------- #


# 1. Write data to Database
def write_to_db_station(stations):
    """
    Write the dynamic data of station into table availability

    :param stations: requests.Response, str, list, dict.
    Should be called only once.
    """
    # transfer data format to ensure process
    try:
        stations = transfer_to_json(stations)
    except TypeError as e:
        print(e)

    # connect to database
    try:
        with engine.connect() as connection:
            for station in stations:
                # get values of a station and insert
                vals = {
                    "number": int(station.get("number")),
                    "name": station.get("name"),
                    "address": station.get("address"),
                    "position_lat": float(station["position"]["lat"]),
                    "position_lng": float(station["position"]["lng"]),
                    "bike_stands": int(station.get("bike_stands")),
                    "banking": station.get("banking"),
                    "bonus": station.get("bonus"),
                }
                sql = """
                INSERT OR IGNORE INTO station (number,name,address, position_lat,position_lng,bike_stands,banking, bonus) 
                VALUES (:number, :name, :address, :position_lat, :position_lng, :bike_stands, :banking, :bonus);
                """
                connection.execute(text(sql), vals)

            # commit changes
            connection.commit()
            print(
                f"stations inserted successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

    except SQLAlchemyError as e:
        print(
            f"station insert failing at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)


def write_to_db_avail(stations):
    """
    Write the dynamic data of station into table availability.

    :param stations: requests.Response, str, list, dict.
    Run every 5 minutes after scraping the bike data.
    """
    # transfer data format to ensure process
    try:
        stations = transfer_to_json(stations)
    except TypeError as e:
        print(e)

    # connect to database
    try:
        with engine.connect() as connection:
            for station in stations:
                # change timestamp into sql format
                last_update = datetime.now()

                # get values of a station and insert
                vals = {
                    "number": int(station.get("number")),
                    "available_bikes": int(station.get("available_bikes")),
                    "available_bike_stands": int(station.get("available_bike_stands")),
                    "last_update": last_update,
                    "status": station.get("status"),
                }

                sql = """
                    INSERT OR IGNORE INTO availability (number,available_bikes,available_bike_stands, last_update,status) 
                    VALUES (:number, :available_bikes, :available_bike_stands, :last_update, :status);
                """
                connection.execute(text(sql), vals)

            # delete the old data
            cutoff = datetime.now() - timedelta(days=7)
            connection.execute(
                text("DELETE FROM availability WHERE last_update < :cutoff"),
                {"cutoff": cutoff}
            )

            # commit all the changes
            connection.commit()
            print(
                f"Availibility updated successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

    except SQLAlchemyError as e:
        print(
            f"Fail to update availability at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)


def write_to_db_current_weather(weather):
    """
    Write the data of current weather into table staion

    :param weather: requests.Response, str, list, dict.
    """
    # transfer data format to ensure process
    try:
        weather = transfer_to_json(weather)
    except TypeError as e:
        print(e)

    # connect to database
    try:
        with engine.connect() as connection:

            # get values of a station and insert
            vals = {
                "dt": weather.get("time"),
                "temperature": weather.get("temperature"),
                "windspeed": weather.get("windspeed"),
                "appearent_temperature": weather.get("appearent_temperature"),
                "weathercode": weather.get("weathercode"),
            }

            sql = """
                INSERT OR IGNORE INTO current_weather (dt,temperature,windspeed,appearent_temperature,weathercode) 
                VALUES (:dt,:temperature,:windspeed,:appearent_temperature,:weathercode);
            """
            connection.execute(text(sql), vals)

            # delete the old data
            cutoff = datetime.now() - timedelta(hours=48)
            connection.execute(
                text("DELETE FROM current_weather WHERE dt < :cutoff"),
                {"cutoff": cutoff}
            )
            # commit all the changes
            connection.commit()
            print(
                f"current_weather updated successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

    except SQLAlchemyError as e:
        print(
            f"Fail to update current_weather at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)


def write_to_db_forecast_hourly(weathers):
    """
    Write the data of forecast weather into table staion

    :param weathers: requests.Response, str, list, dict.
    """
    # transfer data format to ensure process
    try:
        weathers = transfer_to_json(weathers)
    except TypeError as e:
        print(e)

    # connect to database
    try:
        with engine.connect() as connection:

            for weather in weathers:

                # get values of a station and insert
                vals = {
                    "dt": weather.get("time"),
                    "temperature": weather.get("temperature"),
                    "windspeed":weather.get("windspeed"),
                    "weathercode": weather.get("weathercode")
                }

                sql = """
                    INSERT INTO forecast_hourly (dt,temperature,windspeed,weathercode) 
                    VALUES (:dt,:temperature,:windspeed,:weathercode)
                        ON CONFLICT(dt) DO UPDATE SET
                            temperature = excluded.temperature,
                            windspeed = excluded.windspeed,
                            weathercode = excluded.weathercode;
                """
                connection.execute(text(sql), vals)

            # delete the old data
            cutoff = datetime.now()
            connection.execute(
                text("DELETE FROM forecast_hourly WHERE dt < :cutoff"),
                {"cutoff": cutoff}
            )

            # commit all the changes
            connection.commit()
            print(
                f"forecast_hourly updated successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

    except SQLAlchemyError as e:
        print(
            f"Fail to update forecast_hourly at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)


def write_to_db_forecast_daily(weathers):
    """
    Write the data of forecast weather into table staion

    :param weathers: requests.Response, str, list, dict.
    """
    # transfer data format to ensure process
    try:
        weathers = transfer_to_json(weathers)
    except TypeError as e:
        print(e)
        return

    # connect to database
    try:
        with engine.connect() as connection:

            for weather in weathers:
                # get values of a station and insert
                vals = {
                    "dt": weather.get("date"),
                    "temp_max": weather.get("temp_max"),
                    "temp_min": weather.get("temp_min"),
                    "weathercode": weather.get("weathercode"),
                }

                sql = """
                    INSERT INTO forecast_daily (dt,temp_max,temp_min,weathercode) 
                    VALUES (:dt,:temp_max,:temp_min,:weathercode)
                        ON CONFLICT(dt) DO UPDATE SET
                            temp_max = excluded.temp_max,
                            temp_min = excluded.temp_min,
                            weathercode = excluded.weathercode;
                """
                connection.execute(text(sql), vals)

            # delete the old data
            cutoff = datetime.now().date()
            connection.execute(
                text("DELETE FROM forecast_daily WHERE dt < :cutoff"),
                {"cutoff": cutoff}
            )

            # commit all the changes
            connection.commit()
            print(
                f"forecast_daily updated successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

    except SQLAlchemyError as e:
        print(
            f"Fail to update forecast_daily at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)


def transfer_to_json(data):
    if isinstance(data, str):
        return json.load(data)
    elif isinstance(data, requests.Response):
        return data.json()
    elif isinstance(data, (list, dict)):
        return data
    else:
        raise TypeError("Invalid data format.")

# --------------------- Functions for user-related features--------------------- #

def create_user(userdata: dict):
    """
    Write user data to database when creating user account.

    :param userdata: dict,
    return 1 if succeeds.
    return -1 if email already exsists.
    return 0 if fails of other errors.
    """

    email = None
    password = None

    try:
        userdata = transfer_to_json(userdata)
        email = userdata.get("email")
        password = userdata.get("password")
    except TypeError as e:
        print(e)

    print(f"Email: {email}, Password: {password}")  # check these are coming through

    if not email or not password:
        return 0

    try:
        with engine.connect() as connection:
            connection.execute(
                text(
                    "INSERT INTO user (email, password, token) VALUES (:email, :password, :token)"
                ),
                {
                    "email": email,
                    "password": hash_password(password),
                    "token": str(uuid.uuid4()),
                },
            )
            connection.commit()
            return 1

    except IntegrityError as e:
        print("IntegrityError: ", e)
        if "email" in str(e.orig):
            return -1
        return 0

    except SQLAlchemyError as e:
        print("SQLAlchemyError: ", e)
        return 0


def update_user_data(userdata: dict):
    """
    Update user data.

    :param userdata: dict,
    return 1 if succeeds else 0.
    """
    try:
        userdata = transfer_to_json(userdata)
    except TypeError as e:
        print(e)

    # connect to database
    try:
        with engine.connect() as connection:
            set_clause = ", ".join(
                [f"{k} = :{k}" for k in userdata.keys() if k != "uid"]
            )
            sql = text(f"UPDATE user SET {set_clause} WHERE id = :uid")
            connection.execute(sql, userdata)
            connection.commit()
            return 1
    except IntegrityError as e:
        connection.rollback()
        print("Error: ", e)
        error_msg = str(e.orig)
        if "email" in error_msg:
            return -1
        return 0
    except SQLAlchemyError as e:
        connection.rollback()
        print(
            f"Fail to insert user account at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)
        return 0


def write_to_db_favorite(uid, station_number):
    """
    Write user data station to database when saving station.

    :param username:str,
    :param station_number:int,
    return 1 if succeed else 0.
    """

    # connect to database
    try:
        with engine.connect() as connection:
            vals = {"user_id": uid, "station_number": station_number}
            sql = text(
                """
                INSERT OR IGNORE INTO favorite (user_id,station_number)
                VALUES(:user_id,:station_number)
                """
            )
            connection.execute(sql, vals)
            connection.commit()
            return 1

    except SQLAlchemyError as e:
        print(
            f"Fail to insert user account at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)
        return 0


def read_user_security(username):
    """
    Return the password and token of a specific user.
    """
    try:
        with engine.connect() as connection:
            sql = text(
                """SELECT id as uid, email as username, password,token
                    FROM user
                    WHERE email=:username
            """
            )
            result = (
                connection.execute(sql, {"username": username}).mappings().fetchone()
            )
            user_safety = {}
            if result:
                user_safety = dict(result)
            return user_safety

    except SQLAlchemyError as e:
        print(
            f"Fail to get user data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)
        return {}


def read_user_data(uid):
    """
    Read user data from database except safety data.
    """
    try:
        with engine.connect() as connection:
            sql = text(
                """SELECT id,email,token, avatar_url as avatar
                    FROM user
                    WHERE email=:uid
            """
            )
            result = connection.execute(sql, {"uid": uid}).mappings().fetchone()
            user_data = {}
            if result:
                user_data = dict(result)
            if not user_data:
                return user_data
            sql = text(
                "SELECT number, name FROM station, favorite WHERE user_id=:uid and number=station_number"
            )
            result = connection.execute(sql, {"uid": user_data["id"]}).mappings().all()
            if result:
                user_data["favorites"] = [
                    {"number": row["number"], "name": row["name"]} for row in result
                ]
            else:
                user_data["favorites"] = []
            return user_data

    except SQLAlchemyError as e:
        print(
            f"Fail to get user data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)
        return {}


# --------------------- Functions for getting data from database--------------------- #

def read_stations():
    """
    Return the list of stations with their newest data.
    """
    try:
        with engine.connect() as connection:
            sql = text(
                """SELECT s.number as id, s.name, s.position_lat as lat, s.position_lng as lng, 
                     c.available_bikes as bikes, c.available_bike_stands as stands, c.last_update as updated
            FROM station s
            JOIN (SELECT a.number, a.available_bikes, a.available_bike_stands, a.last_update, a.status
            FROM availability a
            INNER JOIN (
                SELECT number, MAX(last_update) as max_update
                FROM availability
                GROUP BY number
            ) b ON a.number = b.number AND a.last_update = b.max_update) c ON s.number= c.number
            """
            )
            result = connection.execute(sql).mappings().all()
            stations = []
            if result:
                for row in result:
                    row = dict(row)
                    updated = row["updated"]
                    if isinstance(updated, str):
                        try:
                            updated = datetime.strptime(updated, "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            updated = datetime.fromisoformat(updated)
                    row["updated"] = int(updated.timestamp())*1000
                    stations.append(row)
            return stations
    except SQLAlchemyError as e:
        print(
            f"Fail to read data of stations at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)
        return []


def read_station_history(station_number):
    """
    Return the historical data of last 24 hours of single select station.

    :param station_number: int, number of the selected station.
    """
    try:
        with engine.connect() as connection:

            # Compute bounds in Python to avoid SQLite localtime quirks
            upper = datetime.now()
            lower = upper - timedelta(hours=24)

            # get hourly history data
            sql = text(
                """
            SELECT
                strftime('%d-%m-%Y %H:00:00', last_update) as hour,
                ROUND(AVG(available_bikes),2) as bikes,
                ROUND(AVG(available_bike_stands),2) as stands
            FROM availability
            WHERE number = :n
            AND last_update >= :lower
            AND last_update < :upper
            GROUP BY hour
            ORDER BY MIN(last_update);
        """
            )
            hourly = connection.execute(sql, {"n": station_number, "lower": lower, "upper": upper}).mappings().all()
            result = []
            if hourly:
                for row in hourly:
                    row = dict(row)
                    dt_obj = datetime.strptime(row["hour"], "%d-%m-%Y %H:00:00")
                    hour = dt_obj.strftime("%H:00")
                    bikes = float(row["bikes"]) if row["bikes"] else 0
                    stands = float(row["stands"]) if row["stands"] else 0
                    result.append({"time": hour, "bikes": bikes, "stands": stands})
            return result

    except SQLAlchemyError as e:
        print(
            f"Fail to read data of availability at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)
        return []


def read_daily_average(station_number):
    """
    Return the historical data of last 7 days) of single select station.

    :param station_number: int, number of the selected station.
    """
    try:
        with engine.connect() as connection:

            # Compute bound in Python to avoid SQLite localtime quirks
            lower = datetime.now() - timedelta(days=7)

            # get daily history data
            sql = text(
                """
                SELECT
                    DATE(last_update) AS date,
                    ROUND(AVG(available_bikes),2) as bikes,
                    ROUND(AVG(available_bike_stands),2) as stands
                FROM availability
                WHERE number = :n AND last_update > :lower
                GROUP BY date
                ORDER BY MIN(last_update);
            """
            )
            daily = connection.execute(sql, {"n": station_number, "lower": lower}).mappings().all()

            result = []
            if daily:
                for row in daily:
                    row = dict(row)
                    date_val = row["date"]
                    if isinstance(date_val, str):
                        date_val = datetime.strptime(date_val, "%Y-%m-%d").date()
                    date = date_val.strftime("%a")
                    bikes = float(row["bikes"]) if row["bikes"] else 0
                    stands = float(row["stands"]) if row["stands"] else 0
                    result.append({"weekday": date, "bikes": bikes, "stands": stands})
            return result
    except SQLAlchemyError as e:
        print(
            f"Fail to read data of availability at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)
        return []


def read_current_weather():
    try:
        with engine.connect() as connection:
            sql = text(
                """SELECT dt as time, temperature, windspeed, appearent_temperature,weathercode
                    FROM current_weather 
                    ORDER BY dt DESC
                    LIMIT 1"""
            )
            result = connection.execute(sql).mappings().fetchone()
            if result:
                result = dict(result)
                time_val = result["time"]
                if isinstance(time_val, str):
                    time_val = datetime.strptime(time_val, "%Y-%m-%d %H:%M:%S")
                result["time"] = time_val.strftime("%Y-%m-%dT%H:%M")
            return result if result else {}
    except SQLAlchemyError as e:
        print(
            f"Fail to read data of current_weather at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)
        return {}


def read_forecast_hourly():
    try:
        with engine.connect() as connection:
            sql = text(
                "SELECT dt as time, temperature, weathercode FROM forecast_hourly"
            )
            result = connection.execute(sql).mappings().all()
            weathers = []
            if result:
                for row in result:
                    weather = dict(row)
                    time_val = weather["time"]
                    if isinstance(time_val, str):
                        time_val = datetime.strptime(time_val, "%Y-%m-%d %H:%M:%S")
                    weather["time"] = time_val.strftime("%Y-%m-%dT%H:%M")
                    weathers.append(weather)
            return {"hourly": weathers}
    except SQLAlchemyError as e:
        print(
            f"Fail to read data of forecast_hourly at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)
        return {}


def read_forecast_daily():
    try:
        with engine.connect() as connection:
            sql = text(
                "SELECT dt as date, temp_max, temp_min, weathercode FROM forecast_daily"
            )
            result = connection.execute(sql).mappings().all()
            weathers = []
            if result:
                for row in result:
                    weather = dict(row)
                    date_val = weather["date"]
                    if isinstance(date_val, str):
                        date_val = datetime.strptime(date_val, "%Y-%m-%d").date()
                    weather["date"] = date_val.strftime("%Y-%m-%d")
                    weathers.append(weather)
            return weathers
    except SQLAlchemyError as e:
        print(
            f"Fail to read data of forecast_daily at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)
        return []

# --------------------- Functions for direction--------------------- #

def find_nearest(lat, lng):
    """Find the nearest station of a given position. Return number,lat and lng of the station"""
    try:
        with engine.connect() as connection:
            sql = text(
                """SELECT s.number as id,
                                s.name,
                                s.position_lat as lat,
                                s.position_lng as lng,
                                c.available_bikes as bikes,
                                c.available_bike_stands as stands
                    FROM station s
                    JOIN (SELECT a.number, a.available_bikes, a.available_bike_stands, a.last_update
                    FROM availability a
                    INNER JOIN (
                        SELECT number, MAX(last_update) as max_update
                        FROM availability
                        GROUP BY number
                    ) b ON a.number = b.number AND a.last_update = b.max_update) c ON s.number= c.number
                    """
            )
            result = connection.execute(sql).mappings()
            if result:
                stations = [dict(row) for row in result]
            else:
                return {}
        nearst = {}
        distance_sqr = float("INF")
        for station in stations:
            d_sqr = (station["lat"] - lat) ** 2 + (station["lng"] - lng) ** 2
            if d_sqr < distance_sqr and station["bikes"] > 0:
                distance_sqr = d_sqr
                nearst = station
        return nearst
    except SQLAlchemyError as e:
        print(
            f"Fail to read data from availability at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)
        return {}


def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def read_for_prediction(station_id):
    '''
    Return the data for bike prediction.

    '''
    try:
        with engine.connect() as connection:
            sql = text("""
                       SELECT number as station_id, bike_stands as capacity 
                        FROM station 
                        WHERE number=:n;
                    """
                    )
            station_result = connection.execute(sql,{"n": station_id}).mappings().fetchone()
            station={}
            if station_result:
                station=dict(station_result)
            sql = text("""
                       SELECT dt as time, temperature, weathercode
                        FROM forecast_hourly ORDER BY dt LIMIT 10;
                    """
                    )
            weather_result = connection.execute(sql,{"n": station_id}).mappings().all()
            weather={
                    "time":[],
                    "temperature":[],
                    "weathercode":[]
                     }
            if weather_result:
                for row in weather_result:
                    row=dict(row)
                    time=row['time']
                    if isinstance(time, str):
                        time=datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                    time=time.strftime("%Y-%m-%d %H:%M:%S")
                    weather["time"].append(time)
                    weather["temperature"].append(row["temperature"])
                    weather["weathercode"].append(row["weathercode"])

            return (station,weather)
    except SQLAlchemyError as e:
        print(
            f"Fail to read data for prediction at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("Error: ", e)
        return ({},{})
