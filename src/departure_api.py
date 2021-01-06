import mvg_api

station_id : str
station_string : str
departures = []

def set_station_id(name : str):
    global station_id
    station_id = mvg_api.get_id_for_station(name)

def set_station_string(name : str):
    global station_string
    station_string = name

def fetch_departures(id : str, offset=0):
    global departures
    departures = mvg_api.get_departures(id, timeoffset=offset)
    #print(departures)
#station_id = get_station_id("Rockefellerstraße")
#depatures = mvg_api.get_departures(station_id)
#print(station_id)
#print(depatures)