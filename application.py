import os, requests
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        #Loading the PM2.5 data from epa
        read = requests.get("https://data.epa.gov.tw/api/v1/aqx_p_02?sort=county&api_key=6af57580-e1d8-47bb-9a78-55b08ae953c9")
        list_read = read.json()
        data = list_read["records"]

        #Rearray the data
        values = list()
        for i in data:
            info = dict()
            info["county"] = i["county"]
            info["Site"] = i["Site"]
            info["PM25"] = i["PM25"]
            values.append(info)
            county = i["county"]
            Site = i["Site"]
            PM25 = i["PM25"]
            #db.execute("INSERT INTO data(county, Site, PM25) VALUES (?, ?, ?)", county, Site, PM25)
            db.execute("UPDATE data SET PM25=:PM25 WHERE Site=:Site",
                        Site = Site, PM25 = PM25)
        return render_template("index.html", values = values)



@app.route("/map", methods =["GET","POST"])
def datamap():
    if request.method == "POST":
        return render_template("map.html")

    else:
        #request the api from epa
        r = requests.get("https://data.epa.gov.tw/api/v1/aqx_p_07?api_key=6af57580-e1d8-47bb-9a78-55b08ae953c9")

        #read in json
        list_r = r.json()

        #change the format in list
        site = list_r["records"]

        #update the Latitude and Longtitude for every site
        for i in site:
            Lat = i["TWD97Lat"]
            Long = i["TWD97Lon"]
            Site = i["SiteName"]
            #db.execute("UPDATE data SET Lat=:Lat, Long=:Long WHERE Site=:Site", Lat = Lat, Long = Long, Site = Site)

        return render_template("map.html")

        #draw the site map
        # circle_map = folium.Map([24.001127,120.885853], zoom_start=8)
        # Site = db.execute("SELECT Site FROM data").tolist()
        # Long = db.execute("SELECT Long FROM data").tolist()
        # Lat = db.execute("SELECT Lat FROM data").tolist()
        # Radius = db.execute("SELECT PM25 FROM data").tolist()
        # for i in range(0, len(Site), 1):
        #     name = Site[i]
        #     R = Radius[i] * 5
        #     coordinate = [Lat[i], Long[i]]
        #     if R >= 45 * 5:
        #         folium.Circle(
        #             coordinate,
        #             radius = R,
        #             fill = True,
        #             popup = name,
        #             color = 'purple',
        #             fill_opacity = 0.8).add_to(circle_map)
        #     elif 35*5 <= R < 45*5:
        #         folium.Circle(
        #             coordinate,
        #             radius = R,
        #             fill = True,
        #             popup = name,
        #             color = 'red',
        #             fill_opacity = 0.8).add_to(circle_map)
        #     elif 20*5 <= R < 35*5:
        #         folium.Circle(
        #             coordinate,
        #             radius = R,
        #             fill = True,
        #             popup = name,
        #             color = '#FF7FF0',
        #             fill_opacity = 0.8).add_to(circle_map)
        #     elif 15*5 <= R < 20*5:
        #         folium.Circle(
        #             coordinate,
        #             radius = R,
        #             fill = True,
        #             popup = 'yellow',
        #             fill_opacity = 0.8).add_to(circle_map)
        #     elif R <= 15*5:
        #         folium.Circle(
        #             coordinate,
        #             radius = R,
        #             fill = True,
        #             popup = '#00FF00',
        #             fill_opacity = 0.8).add_to(circle_map)

        #     circle_map.save('map.html')
        #     return render_template("map.html")

