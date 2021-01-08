import tkinter as tk
from datetime import datetime
import json_loader
import weather_api
import calendar_api
import departure_api
import webbrowser
import time, os, dateutil.parser
from PIL import ImageTk, Image

class Main:
    background_color = "#ffffff"
    header_color = "#666666"
    frame_color = "#000000"
    font = ""

    def __init__(self):
        json_loader.load_data()
        self.init_gui()
        
        self.init_weather_api()
        self.update_weather_loop()

        self.init_calendar_api()
        self.update_calendar_loop()

        self.init_departures_api()
        self.update_departures_loop()

        self.mainloop()

    def mainloop(self):
        self.root.mainloop()

    def load_style_json(self):
        self.font = json_loader.font
        self.background_color = json_loader.background_color
        self.frame_color = json_loader.frame_color
        self.header_color = json_loader.header_color
        self.highlight_color = json_loader.highlight_color

    def init_departures_api(self):
        station_string = json_loader.departures_station
        departure_api.set_station_string(station_string)
        departure_api.set_station_id(station_string)

    def link_to_departures(self):
        webbrowser.open_new_tab("https://www.mvg.de/dienste/abfahrtszeiten.html#mvg-live-stationID=" + departure_api.station_id)

    def update_departures(self):
        departure_api.fetch_departures(departure_api.station_id)
        #print(departure_api.departures[0])

        c = 0
        for field in self.event_labels_departures:
            dep = departure_api.departures[c]
            #times:
            time = dep["departureTime"]
            delay = dep["delay"]
            dt = datetime.fromtimestamp(time / 1000)
            #print(readable_time.strftime("%H:%M"))
            field[0].config(text = dt.strftime("%H:%M (+{0}min): ".format(delay)))
            c += 1

            #info:
            line = dep["label"]
            line_color = dep["lineBackgroundColor"]
            dest = dep["destination"]
            min_left = dep["departureTimeMinutes"]

            field[1].config(text = line, bg=line_color)
            field[2].config(text="{0} ({1}min)".format(dest, min_left))


    def update_departures_loop(self):
        print("Getting Departures [loop]")
        self.update_departures()
        #loop:
        self.root.after(60000, self.update_departures_loop)

    def init_calendar_api(self):
        calendar_api.login()
        calendar_api.calendarID = json_loader.calendarID

    def link_to_calendar(self):
        webbrowser.open_new_tab(json_loader.calendarURL)

    def update_calendar(self):
        #print("Id:" + calendar_api.calendarID)

        calendar_api.fetch_data()
        events = calendar_api.upcoming_events

        c = 0
        today = datetime.now().date()

        #print(len(events))
        for event in events:
            #start_utc = dateutil.parser.parse(start)
            #print(start_utc.strftime("%d.%m.%Y %H:%M"))
            #print(start, event['summary'])
            #print(start_utc.strftime("%d.%m.%Y %H:%M"), event["summary"])
            event_start = dateutil.parser.parse(event[0])
            event_date = event_start.date()

            #remove the 00:00 if the event starts at midnight/whole-day whatever. datetime.time doesn't want to work
            event_start_str = event_start.strftime("%d.%m.%Y %H:%M")
            if "00:00" in event_start_str:
                event_start_str = event_start_str.replace(" 00:00", ":")
            else:
                event_start_str = event_start_str + "Uhr:"

            #Today's the day!    
            if (today == event_date):
                self.event_labels_calendar[c][0].configure(fg=self.highlight_color)
                self.event_labels_calendar[c][1].config(fg=self.highlight_color)

            self.event_labels_calendar[c][0].configure(text=event_start_str)
            self.event_labels_calendar[c][1].configure(text="{}".format(event[1]))

            c += 1

    def update_calendar_loop(self):
        print("getting calendar update [loop]")
        self.update_calendar()
        #==loop==
        self.root.after(180000, self.update_calendar_loop)

    def init_weather_api(self):
        self.weather_api = weather_api.Weather_api()
        self.weather_api.set_api_key(json_loader.api_key)
        self.weather_api.set_lat(json_loader.lat)
        self.weather_api.set_lon(json_loader.lon)

    def update_weather_loop(self):
        print("getting weather [loop]")
        self.update_weather()
        #===loop===
        self.root.after(180000, self.update_weather_loop)

    def update_weather(self):
        print("updateing weather.")
        self.weather_api.fetch_weather_data()
        temp = str(self.weather_api.get_current_temp())+"°C (feels like: " + str(self.weather_api.get_current_feels_like()) + "°C)"
        pressure = str(self.weather_api.get_current_pressure()) + "hpa"
        self.tmp_lbl_today.configure(text = temp)
        self.prs_lbl_today.configure(text = pressure)
        
        icon = self.weather_api.get_current_image()
        p = "/assets/weather_icons/{}@2x.png".format(icon)
        self.weather_icon_current = ImageTk.PhotoImage(Image.open(os.path.normpath(os.getcwd() + os.sep + p)))
        self.weather_icon_current_label.configure(image=self.weather_icon_current)

        #today min-max
        min, max = self.weather_api.get_today_min_max()
        self.tmp_lbl_today_min_max.configure(text="{0}°C / {1}°C".format(min, max))

        #description
        self.weather_icon_current_subtext.configure(text=self.weather_api.get_current_description())

        #===Future===
        min, max = self.weather_api.get_tomorrow_min_max()
        self.tmp_lbl_tomorrow.configure(text="{0}°C ({1}°C to {2}°C \u2014 {3})"
            .format(str(self.weather_api.get_tomorrow_temp()), min, max, self.weather_api.get_tomorrow_description()))

    def link_to_weather(self):
        webbrowser.open_new_tab("https://openweathermap.org/city/" + json_loader.city_name)

    #==============GUI====================        
    def init_gui(self):
        self.load_style_json()
        self.root = tk.Tk()
        self.root.geometry("1000x750+{0}+{1}".format(json_loader.offset[0], json_loader.offset[1]))
        self.root.configure(bg=self.background_color)
        self.root.resizable(False, False)
        #self.root.overrideredirect(True)

        ###====images====
        #for instant-reloads of a frame:
        self.refresh_img = ImageTk.PhotoImage(file=os.path.normpath(os.getcwd() + os.sep + "/assets/refresh.png"))

        #calendar-img
        self.calendar_link_img = ImageTk.PhotoImage(file=os.path.normpath(os.getcwd() + os.sep + "/assets/calendar.png"))
    	#weather_img
        self.weather_link_img = ImageTk.PhotoImage(file=os.path.normpath(os.getcwd() + os.sep + "/assets/weather.png"))
        #departures_img
        self.departures_link_img = ImageTk.PhotoImage(file=os.path.normpath(os.getcwd() + os.sep + "/assets/departures.png"))

        #Title:
        self.greeting = "Hello, {}!".format(json_loader.username)
        self.root.title(self.greeting)  

        #Top bar:
        self.header = tk.Frame(master=self.root, width=1000, height=50, bg=self.header_color, highlightthickness=0)
        self.header.grid_propagate(0)
        self.header.pack(side="top")

        tk.Label(master=self.header, text='Dashboard', font=(self.font, 30), bg=self.header_color, fg='white').grid(column=0, row=0, sticky="w")

        #Top bar (time)
        self.time_label = tk.Label(master=self.header, text="", font=(self.font, 15), bg=self.header_color, fg="white")
        self.time_label.grid(column=1, row=0)
        self.time()

        #Top bar (date)
        self.date_label = tk.Label(self.header, text=datetime.now().strftime('%A, %d. %B %Y'), font=(self.font, 20), bg=self.header_color, fg='white')
        self.date_label.grid(column=2, row=0, sticky="e")
        
        self.header.columnconfigure(0, weight=1)
        self.header.columnconfigure(1, weight=1)
        self.header.columnconfigure(2, weight=1)

        #=========================Weather====================================
        self.weather = tk.Frame(self.root, width=450, height=180, bg="blue")
        self.weather.place(x=20, y=70)

        #title
        self.weather_top = tk.Frame(self.weather, width=450, height=30, bg=self.header_color)
        self.weather_top.pack(side="top", anchor="w")
        self.weather_top.pack_propagate(0)
        tk.Label(self.weather_top, text="Weather in {}".format(json_loader.city_name), font=(self.font, 15), bg=self.header_color, fg="white").pack(side="left")

        #refresh-button:
        btn_refresh_weather = tk.Button(self.weather_top, text="R", image=self.refresh_img, command=self.update_weather, bg=self.header_color, activebackground=self.header_color)
        btn_refresh_weather.pack(side="right", padx=2)

        #website-link
        btn_link_weather = tk.Button(self.weather_top, text="L", image=self.weather_link_img, command=self.link_to_weather, bg=self.header_color, activebackground=self.header_color)
        btn_link_weather.pack(side="right", padx=2)

        #body
        self.weather_body = tk.Frame(self.weather, width=450, height=150, bg=self.frame_color)
        self.weather_body.pack(side="top", anchor="w")
        self.weather_body.pack_propagate(0)

        #icon
        self.weather_icon_body = tk.Frame(self.weather_body, bg=self.frame_color)
        self.weather_icon_body.pack(side="right")

        self.weather_icon_current = ImageTk.PhotoImage(Image.open(os.path.normpath(os.getcwd() + os.sep + "/assets/weather_icons/01d@2x.png")))
        self.weather_icon_current_label = tk.Label(self.weather_icon_body, image = self.weather_icon_current, bg=self.frame_color)
        self.weather_icon_current_label.pack(side="top", anchor="e")       
        
        self.weather_icon_current_subtext = tk.Label(self.weather_icon_body, text="-------", font=(self.font, 9), bg=self.frame_color, fg="white")
        self.weather_icon_current_subtext.pack(side="bottom", anchor="center")

        #weather_data_body
        self.weather_data_body = tk.Frame(self.weather_body, bg=self.frame_color, borderwidth=0, highlightthickness=0)
        self.weather_data_body.pack(side="left")

        #===today/now===
        tk.Label(self.weather_data_body, text="Today:", font=(self.font, 16, "underline", "bold"), bg=self.frame_color, fg="white").grid(column=0, row=0, sticky="nw")
        #temperature
        self.tmp_lbl_today = tk.Label(self.weather_data_body, text="0.00°C", font=(self.font, 10, "bold"), bg=self.frame_color, fg="white")
        self.tmp_lbl_today.grid(column=0, row=1, sticky="w")
        #min/max
        self.tmp_lbl_today_min_max = tk.Label(self.weather_data_body, text="MIN°C/MAX°C", font=(self.font, 10), bg=self.frame_color, fg="white")
        self.tmp_lbl_today_min_max.grid(column=0, row=2, sticky="w")
        #pressure
        self.prs_lbl_today = tk.Label(self.weather_data_body, text="0000hpa", font=(self.font, 10, "bold"), bg=self.frame_color, fg="white")
        self.prs_lbl_today.grid(column=1, row=1, sticky="e")
        
        #===future===
        tk.Label(self.weather_data_body, text="Tomorrow:", font=(self.font, 12, "bold"), bg=self.frame_color, fg="white").grid(column=0, row=3, sticky="w")
        #this i just a one-liner:
        self.tmp_lbl_tomorrow = tk.Label(self.weather_data_body, text="------", font=(self.font, 8, "italic"), bg=self.frame_color, fg="white")
        self.tmp_lbl_tomorrow.grid(column=0, row=4, sticky="w")

        #===============Calendar========================
        self.calendar = tk.Frame(self.root, width=450, height=300, bg="blue")
        self.calendar.place(x=530, y=70)

        #title
        self.calendar_top = tk.Frame(self.calendar, width=450, height=30, bg=self.header_color)
        self.calendar_top.pack(side="top", anchor="w")
        self.calendar_top.pack_propagate(0)
        tk.Label(self.calendar_top, text="Calendar", font=(self.font, 15), bg=self.header_color, fg="white").pack(side="left")
    	
        #refresh button:
        btn_refresh = tk.Button(self.calendar_top, text="R", image=self.refresh_img, command=self.update_calendar, bg=self.header_color, activebackground=self.header_color)
        btn_refresh.pack(side="right", padx=2)
        #link:
        btn_link_calendar = tk.Button(self.calendar_top, text="L", image=self.calendar_link_img, command=self.link_to_calendar, bg="white", activebackground=self.header_color)
        btn_link_calendar.pack(side="right", padx=2)
        #body
        self.calendar_body = tk.Frame(self.calendar, width=450, height=270, bg=self.frame_color, padx=3, pady=2)
        self.calendar_body.pack(side="top", anchor="w", fill="x")
        #self.calendar_body.grid_propagate(0)
        self.calendar_body.columnconfigure(1, weight=1)

        self.event_labels_calendar = []
        i = 0
        while (i < 10):
            date_label = tk.Label(self.calendar_body, text="01.01.1971", font=(self.font, 11, "italic"), bg=self.frame_color, fg="white")
            date_label.grid(row=i, column=0, sticky="w")

            description_label = tk.Label(self.calendar_body, text="HELLO THERE!", 
                font=(self.font, 10), bg=self.frame_color, fg="black")
            description_label.grid(row=i, column=1, sticky="w")

            self.event_labels_calendar.append((date_label, description_label))
            i += 1
        #print(self.event_labels)


        #=========================Departures====================================
        self.departures = tk.Frame(self.root, width=450, height=180, bg="blue")
        self.departures.place(x=20, y=270)

        #title
        self.departures_top = tk.Frame(self.departures, width=450, height=30, bg=self.header_color)
        self.departures_top.pack(side="top", anchor="w")
        self.departures_top.pack_propagate(0)
        text = "Departures from {}".format(json_loader.departures_station)
        tk.Label(self.departures_top, text=text, font=(self.font, 15), bg=self.header_color, fg="white").pack(side="left")
        
        #refresh
        btn_refresh = tk.Button(self.departures_top, text="R", image=self.refresh_img, command=self.update_departures, bg=self.header_color, activebackground=self.header_color)
        btn_refresh.pack(side="right", padx=2)

        #link:
        btn_link_departures = tk.Button(self.departures_top, text="L", image=self.departures_link_img, command=self.link_to_departures, bg=self.header_color, activebackground=self.header_color)
        btn_link_departures.pack(side="right", padx=2)
        
        #body
        self.departures_body = tk.Frame(self.departures, width=450, height=150, bg=self.frame_color)
        self.departures_body.pack(side="top", anchor="w", fill="x")
        
        #self.departures_body.pack_propagate(0)

        self.event_labels_departures = []
        i = 0
        while (i < 5):
            date_label = tk.Label(self.departures_body, text="01.01.1971", font=(self.font, 11, "italic"), bg=self.frame_color, fg="white")
            date_label.grid(row=i, column=0, sticky="w")

            line_label = tk.Label(self.departures_body, text="000", font=(self.font, 10), bg=self.frame_color, fg="white", 
                borderwidth=2, relief="raised")
            line_label.grid(row=i, column=1, sticky="w", pady=2)

            description_label = tk.Label(self.departures_body, text="HELLO THERE!", 
                font=(self.font, 10), bg=self.frame_color, fg="black")
            description_label.grid(row=i, column=2, sticky="w")

            self.event_labels_departures.append((date_label, line_label, description_label))
            i += 1

        #===============key events======================
        self.root.bind('<Return>', self.KEY_enter) 

    def time(self):
        string = time.strftime("%H:%M:%S %p")
        self.time_label.configure(text = string)
        self.time_label.after(100, self.time)

    def KEY_enter(self, event):
        print("bye.")
        quit()

if __name__ == "__main__":
    main = Main()