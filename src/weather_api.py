import requests, json 

class Weather_api():  
    __api_key = "253cb91132b72532222082116499b2e8"
    
    #base_url variable to store url 
    #base_url = "http://api.openweathermap.org/data/2.5/weather?"
    __base_url = "https://api.openweathermap.org/data/2.5/onecall?"
    __lon = "11.58"
    __lat = "48.14"    
    complete_url = __base_url + "appid=" + __api_key + "&lon=" + __lon + "&lat=" + __lat + "&units=metric"

    def set_api_key(self, k):
        __api_key = k

    def set_lon(self, l):
        __lon = l

    def set_lat(self, l):
        __lat = l


    def fetch_weather_data(self):
        response = requests.get(self.complete_url)
        response = response.json() 
        self.current = response["current"]
        self.hourly = response["hourly"] 
        self.daily = response["daily"]

    def get_current_image(self):
        return self.current["weather"][0]["icon"]

    def get_current_description(self):
        return self.current["weather"][0]["description"]

    def get_current_temp(self):
        return self.current["temp"]

    def get_current_feels_like(self):
        return self.current["feels_like"]

    def get_current_humidity(self):
        return self.current["humidity"]

    def get_current_pressure(self):
        return self.current["pressure"]

    def get_today_min_max(self):
        return self.daily[0]["temp"]["min"], self.daily[0]["temp"]["max"]

    def get_tomorrow_temp(self):
        return self.daily[1]["temp"]["day"]
    
    def get_tomorrow_description(self):
        return self.daily[1]["weather"][0]["description"]

    def get_tomorrow_min_max(self):
        return self.daily[1]["temp"]["min"], self.daily[1]["temp"]["max"]

    #fetch_weather_data()
    #print(get_current_temp())