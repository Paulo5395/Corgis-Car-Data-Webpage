from flask import Flask, url_for, render_template, request
from markupsafe import Markup

import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/p1")
def render_page1():
    cyl_count = get_num_cyl()

    brands = get_brands()

    avg_mpg_by_brand = get_avg_mpg_of_brands(brands)

    num_4_cyl = cyl_count["num_4_cyl"]
    num_5_cyl = cyl_count["num_5_cyl"]
    num_6_cyl = cyl_count["num_6_cyl"]
    num_8_cyl = cyl_count["num_8_cyl"]
    num_10_cyl = cyl_count["num_10_cyl"]
    num_12_cyl = cyl_count["num_12_cyl"]

    engines = get_engines_options()
    engine = request.args.get('engine')

    if 'engine' in request.args:
        data = engine_mileage(engine)

        display_city_data = "City mpg " + str(data[0])
        display_highway_data = "Highway mpg: " + str(data[1])

        print(avg_mpg_by_brand)

        return render_template('page1.html', last_selected = engine, engine_options = engines, city_data = display_city_data, highway_data = display_highway_data, brands = brands, num_4_cyl = num_4_cyl, num_5_cyl = num_5_cyl, num_6_cyl = num_6_cyl, num_8_cyl = num_8_cyl, num_10_cyl = num_10_cyl, num_12_cyl = num_12_cyl)

    return render_template('page1.html', engine_options = engines, num_4_cyl = num_4_cyl, num_5_cyl = num_5_cyl, num_6_cyl = num_6_cyl, num_8_cyl = num_8_cyl, num_10_cyl = num_10_cyl, num_12_cyl = num_12_cyl)

#-------------------------- json Data ---------------------------------------------------

def get_engines_options():
    with open('./static/cars.json') as engines_data:
        cars = json.load(engines_data)
    engines =[]

    for e in cars:
        if e["Engine Information"]["Engine Type"] not in engines:
            engines.append(e["Engine Information"]["Engine Type"])
            engines.sort()
    options =""

    for engine in engines:
        options += Markup("<option value\"" + engine + "\">" + engine + "</options>")
    return options

def engine_mileage(engine):
    with open('./static/cars.json') as mileage_data:
        cars = json.load(mileage_data)
    city_mileage = 0
    highway_mileage = 0

    for e in cars:
        if e["Engine Information"]["Engine Type"] == engine:
            city_mileage = e["Fuel Information"]["City mpg"]
            highway_mileage = e["Fuel Information"]["Highway mpg"]
    return[city_mileage, highway_mileage]

def get_num_cyl():
    with open('./static/cars.json') as cylinder_data:
        engines = json.load(cylinder_data)

    num_cyl = {
        "num_4_cyl": 0,
        "num_5_cyl": 0,
        "num_6_cyl": 0,
        "num_8_cyl": 0,
        "num_10_cyl": 0,
        "num_12_cyl": 0
    }

    for e in engines:
        if "4 cylinder" in e["Engine Information"]["Engine Type"]:
            num_cyl["num_4_cyl"] += 1
        
        elif "5 Cylinder" in e["Engine Information"]["Engine Type"]:
            num_cyl["num_5_cyl"] += 1

        elif "6 cylinder" in e["Engine Information"]["Engine Type"]:
            num_cyl["num_6_cyl"] += 1

        elif "8 cylinder" in e["Engine Information"]["Engine Type"]:
            num_cyl["num_8_cyl"] += 1

        elif "10 cylinder" in e["Engine Information"]["Engine Type"]:
            num_cyl["num_10_cyl"] += 1

        elif "12 cylinder" in e["Engine Information"]["Engine Type"]:
            num_cyl["num_12_cyl"] += 1

    return(num_cyl)

def get_brands():
    with open('./static/cars.json') as brand_data:
        car_data = json.load(brand_data)

    brands = []

    temp = 0

    for c in car_data:

        if c["Identification"]["Make"] not in brands:
            brands.append(c["Identification"]["Make"])
            brands.sort()

    return brands

def get_avg_mpg_of_brands(brands):
    with open('./static/cars.json') as brand_data:
        cars = json.load(brand_data)

        car_count = 0;
        avg_brand_mpg = {}

        for x in cars:

            if x["Identification"]["Make"] not in avg_brand_mpg:
                avg_brand_mpg[x["Identification"]["Make"]] = 1 # (x["Fuel Information"]["City mpg"] + x["Fuel Information"]["Highway mpg"])

            elif x["Identification"]["Make"] in avg_brand_mpg:
                avg_brand_mpg[x["Identification"]["Make"]] += 1


        return avg_brand_mpg



if __name__=="__main__":
    app.run(debug=True)