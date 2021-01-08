# Dashboard
U'll need a key for openweatherapi and get started with the google calendar api. Super easy, barely an inconvenience.
The departures work with the mvg-api, so it only works if you live in munich (well, it works in paris too... But why would you want to know the departures in munich, when you live in paris?)

config-example: 

{
    "name": "Kurt", 
    "languages": ["English", "German"],
    "font": "Montserrat",
    "offset": [2000, 200],
    "colors": 
    {
        "background_color": "#ffb3b3",
        "header_color": "#f24040",
        "frame_color": "#f35858",
        "highlight_color": "#1815b3"
    },
    "weather": 
    {
        "api_key": "00000000000000000000000",
        "lon": "11.58",
        "lat": "48.14",
        "name": "Munich"
    },
    "calendar":
    {
        "ID": "primary",
        "URL": "https://calendar.google.com"
    },
    "departures":
        {
            "station": "Hauptbahnhof"
        }
    
}
