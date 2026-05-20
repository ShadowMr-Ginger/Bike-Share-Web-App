import pandas as pd
import numpy as np
from datetime import datetime

def data_processor(station,weather):
    '''
    Processing the raw data from backend to align with the features required for modeling.

    :station:dict, with key "station_id", "lat","lon","capacity".
    :weather:dict, weather forecast for the next 10 hours, with key "hour","temperature","windspeed","weathercode".
    '''
    try:
        df_station=pd.DataFrame(station, index=[0])
        df_weather=pd.DataFrame(weather)
        df = df_weather.merge(df_station, how="cross")
        df["time"]=pd.to_datetime(df["time"])
        df["hour"] = df["time"].dt.hour
        df["day"]=df["time"].dt.day
        df["day_of_week"] = df["time"].dt.dayofweek
        df["rainy"]=np.where(df["weathercode"]>48,1,0)
        col_to_drop=["time","weathercode"]
        df.drop(col_to_drop,axis=1,inplace=True)
        return df
    except Exception as e:
        print(f"Fail to process data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {e}")
        return None

def predict_next10(model,df):
    '''
    Return the predicted number of bikes and stands for the 10 hours

    :model: trained model
    :df: data frame of required features.
    return a dict of results
    '''
    try:
        features = ['station_id', 'hour', 'day', 'day_of_week', 'temperature', 'rainy']
        preds=model.predict(df[features])
        df["bikes"]=preds
        df["bikes"]=np.where(df["bikes"]>df["capacity"],df["capacity"],df["bikes"])
        df["bikes"]=np.where(df["bikes"]<0,0,df["bikes"])
        df["stands"]=df["capacity"]-df["bikes"]
        df["time"]=df["hour"].map(lambda x: f"{x:02d}:00")
        selected=["time","bikes","stands"]
        result=df[selected].to_dict(orient='records')        
        return result
    except Exception as e:
        print(f"Fail to predict at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {e}")
        return None