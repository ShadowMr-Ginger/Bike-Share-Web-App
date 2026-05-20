import requests
import json
import os
import traceback
from datetime import datetime

# --------------------------------------------------------------------------------#

LAT = 53.3498
LON = -6.2603
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# --------------------------------------------------------------------------------#

# Pulls data from API and saves as a file in 'data'
def get_data(url,param,type):
    '''
    Scrap data with given parameters. If succeed, save data and return response.
    
    :param url: url for web scraping
    :param param: parameters for web scraping
    :param type: "bikes", "current_weather" or "forecast_weather"
    return: requests.Response
    '''
    try:
        # Get API
        response = requests.get(url,params=param)

        if response.status_code == 200:
            # Save to file
            write_to_file(response.text,type)
            print(
                f"Data of {type} logged successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            return response
        else:
            print(f"API Error: {response.status_code}")

    except Exception:
        print("AN ERROR OCCURRED:")
        print(traceback.format_exc())
    
def write_to_file(data,type):
    '''
    Write data to jsonl file, which write the data of the same day into one file
    
    :param data: data to write to the file
    :param type: "bikes", "current_weather", "forecast_hourly" or "forecast_daily"
    '''
    # Create folder for data
    if not os.path.exists("data"):
        os.mkdir("data")
        print("Folder 'data' created!")

    # station time for end of file name
    time_of_pull = datetime.now().strftime("%Y-%m-%d")

    filename = os.path.join("data", f"{type}_{time_of_pull}.jsonl")
    # write to file
    with open(filename, "a") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def get_bike_data():
    params={
    "apiKey": os.getenv('BIKE_API_KEY'), 
    "contract": "dublin"
    }
    url = "https://api.jcdecaux.com/vls/v1/stations"
    bikes=get_data(url,params,"bikes")
    return bikes


def get_current_weather():
    params = {
        "latitude": LAT,
        "longitude": LON,
        "current_weather": True,
        "hourly": "apparent_temperature",
        "timezone": "auto"
    }
    data=get_data(WEATHER_URL,params,"current_weather").json()
    current = data["current_weather"]
    current_hour=current["time"][:13]
    appearent_temp = None
    if "hourly" in data:
        for time_str, temp in zip(
            data["hourly"]["time"],
            data["hourly"]["apparent_temperature"],
        ):  
            if current_hour==time_str[:13]:
                appearent_temp = temp
                break
    current_time=datetime.fromisoformat(current["time"]).strftime('%Y-%m-%d %H:%M:%S')
    return {
        "time": current_time,
        "temperature": current["temperature"],
        "windspeed": current["windspeed"],
        "appearent_temperature": appearent_temp,
        "weathercode": current["weathercode"]
    }

def get_hourly_weather():
    params = {
        "latitude": LAT,
        "longitude": LON,
        "hourly": "temperature_2m,wind_speed_10m,weathercode",
        "forecast_days": 2,
        "timezone": "auto"
    }
    data=get_data(WEATHER_URL,params,"hourly_forecast").json()
    
    now = datetime.now().replace(minute=0, second=0, microsecond=0)

    result = []

    for time_str, temp, windspeed,code in zip(
        data["hourly"]["time"],
        data["hourly"]["temperature_2m"],
        data["hourly"]["wind_speed_10m"],
        data["hourly"]["weathercode"]
    ):
        dt = datetime.fromisoformat(time_str)
        if dt >= now:
            time=datetime.fromisoformat(time_str).strftime('%Y-%m-%d %H:%M:%S')
            result.append({
                "time": time,
                "temperature": temp,
                "windspeed":windspeed,
                "weathercode": code
            })

        if len(result) == 24:
            break

    return result

def get_daily_weather():
    params = {
        "latitude": LAT,
        "longitude": LON,
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "forecast_days": 8,
        "timezone": "auto"
    }
    data=get_data(WEATHER_URL,params,"daily_forecast").json()

    today = datetime.now().date()

    result = []

    for date_str, tmax, tmin, code in zip(
        data["daily"]["time"],
        data["daily"]["temperature_2m_max"],
        data["daily"]["temperature_2m_min"],
        data["daily"]["weathercode"],
    ):
        date_obj = datetime.fromisoformat(date_str).date()

        if date_obj > today:
            result.append({
                "date": date_str,
                "temp_max": tmax,
                "temp_min": tmin,
                "weathercode": code
            })

        if len(result) == 7:
            break

    return result
