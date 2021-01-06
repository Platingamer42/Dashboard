import json
import os

#username = ""


def load_data():
    global username, api_key, lon, lat, city_name, background_color, header_color, frame_color, font, calendarID, calendarURL, departures_station, offset
    path = os.path.join(os.path.realpath(__file__), "..", "..", "config.json")
    #print(path)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    
    #print(data)
    username = data["name"] 
    api_key = data["weather"]["api_key"]

    font = data["font"]
    offset = data["offset"]

    background_color = data["colors"]["background_color"]
    header_color = data["colors"]["header_color"]
    frame_color = data["colors"]["frame_color"]

    lon = data["weather"]["lon"]   
    lat = data["weather"]["lat"]
    city_name = data["weather"]["name"]
    
    calendarID = data["calendar"]["ID"]
    calendarURL = data["calendar"]["URL"]

    departures_station = data["departures"]["station"]
    #print(data)