import requests
import os
import database.db_manager as db
from dotenv import load_dotenv

load_dotenv()

def geocode(addr):
    '''
    Transfer the address into lat and lng.

    :addr: str, addresss
    return lat and lng
    '''
    GOOGLE_KEY=os.getenv('GOOGLE_KEY')
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={addr}&components=country:IE|locality:Dublin&key={GOOGLE_KEY}"
    res = requests.get(url).json()
    if res.get("status") == "OK":
        loc = res["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    raise Exception(f"Geocoding failed for {addr}")

def ors_route(start, end):
    '''
    Get route from openrouteservice.
    :start: tuple of (lat,lng)
    :end: tuple of (lat,lng)
    return route
    '''
    ORS_KEY=os.getenv('ORS_KEY')
    url = "https://api.openrouteservice.org/v2/directions/cycling-regular/geojson"
    body = {"coordinates": [[start[1], start[0]], [end[1], end[0]]]}
    headers = {"Authorization": ORS_KEY, "Content-Type": "application/json"}
    res = requests.post(url, json=body, headers=headers)
    print(res)
    if res.status_code == 200:
        return res.json()
    raise Exception(f"ORS routing failed: {res.text}")

def get_route(from_addr, to_addr):
    '''
    Get route of startpoint to the nearest bike station and the route of the bike station to the endpoint.

    :from_addr: str, address of the startpoint.
    :to_addr:str, addresss of the endpoint.
    return two parts of routes.
    '''
    from_lat, from_lng = geocode(from_addr)
    to_lat, to_lng = geocode(to_addr)
    start_station = db.find_nearest(from_lat, from_lng)
    segment1 = ors_route((from_lat, from_lng), (start_station["lat"], start_station["lng"]))
    segment2 = ors_route((start_station["lat"], start_station["lng"]), (to_lat, to_lng))
    return {
        "segments": [segment1, segment2],
        "stations": {
            "start_station": start_station
        }
    }
