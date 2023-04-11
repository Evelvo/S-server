from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from threading import *
from time import sleep
from waitress import serve

app = Flask(__name__)

temperature = "error"
feels_temp = "error"
rain = "error"
time = "error"
year_day = "error"
week = "error"


id = "1-91664"



URL = f"https://www.yr.no/nb/v%C3%A6rvarsel/daglig-tabell/{id}"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="page-content")


def get_temp():
    try:
        temp = results.find("span", class_="temperature temperature--warm")
        temperatur1 = temp.text.replace("Temperatur", "")
        temperatur1 = temperatur1.replace("°", "")
    except:
        temp = results.find("span", class_="temperature temperature--cold")
        temperatur1 = temp.text.replace("Temperatur", "")
        temperatur1 = temperatur1.replace("°", "")
    
    return temperatur1

def get_now_feels_like():
    feels_temp = results.find("div", class_="feels-like-text")
    feels_temp = feels_temp.text
    feels_temp = feels_temp.replace("Føles som", "")
    feels_temp = feels_temp.replace("°", "")
    return feels_temp
def get_water():
    rain = results.find("span", class_="now-hero__next-hour-precipitation-value")
    rain = rain.text
    return rain


def get_time():
    URL = "https://www.timeanddate.no/klokka/i/norge/knarrevik-straume"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(class_="main-content-div")

    time = results.find("span", id="ct")
    week = "test"
    year_day = "test"
    return [str(time), str(week), str(year_day)]






class get_weather(Thread):
    def run(e):
        global temperature, feels_temp, rain, time, week, year_day

        while True:
            temperature = get_temp()
            feels_temp = get_now_feels_like()
            rain = get_water()
            time = get_time()[0]
            week = get_time()[1]
            year_day = get_time()[2]
            sleep(10)

var_get_weather = get_weather()
var_get_weather.start()



@app.route("/api")
def api():
    return jsonify(
        temperatur = temperature,
        feels_temp = feels_temp,
        rain = rain,
        time = time, 
        week = week,
        year_day = year_day
    )

if __name__ == "__main__":
    #app.run(host = "0.0.0.0", port = 8080)
    serve(app, host="0.0.0.0", port=8080)

