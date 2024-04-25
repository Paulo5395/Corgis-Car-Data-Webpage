from flask import Flask, url_for, render_template, request
from markupsafe import Markup

import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

# @app.route("/")
# def render_main():
#     return render_template('home.html')

@app.route("/")
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

    cars = get_car_options()
    car = request.args.get('car')

    if 'car' in request.args:
        engine_mileage = get_engine_mileage(car)
        engine_info = get_engine_info(car)

        city_mpg = "City mpg: " + str(engine_mileage[0])
        highway_mpg = "Highway mpg: " + str(engine_mileage[1])

        return render_template('home.html', last_selected = car, car_options = cars, 
                                city_mpg = city_mpg, highway_mpg = highway_mpg, 
                                avg_mpg_by_brand = avg_mpg_by_brand, engine_info = engine_info,
                                num_4_cyl = num_4_cyl, num_5_cyl = num_5_cyl, 
                                num_6_cyl = num_6_cyl, num_8_cyl = num_8_cyl, 
                                num_10_cyl = num_10_cyl, num_12_cyl = num_12_cyl)

    return render_template('home.html', car_options = cars,
                             avg_mpg_by_brand = avg_mpg_by_brand, 
                             num_4_cyl = num_4_cyl, num_5_cyl = num_5_cyl, 
                             num_6_cyl = num_6_cyl, num_8_cyl = num_8_cyl, 
                             num_10_cyl = num_10_cyl, num_12_cyl = num_12_cyl)

#-------------------------- Retreving json Data ---------------------------------------------------

def get_engine_info(car):
    with open('./static/cars.json') as brand_data:
        car_data = json.load(brand_data)

    engine_info = ""

    for car_sel in car_data:

        if car_sel["Identification"]["ID"] == car:
            engine_info = car_sel["Engine Information"]["Engine Type"]

    return engine_info

def get_car_options():
    with open('./static/cars.json') as json_data:
        car_data = json.load(json_data)
    cars =[]

    for car in car_data:
        if car["Identification"]["ID"] not in cars:
            cars.append(car["Identification"]["ID"])
            cars.sort()
    options =""

    for car in cars:
        options += Markup("<option value\"" + car + "\">" + car + "</options>")
    return options

def get_engine_mileage(car):
    with open('./static/cars.json') as mileage_data:
        cars = json.load(mileage_data)
    city_mileage = 0
    highway_mileage = 0

    for e in cars:
        if e["Identification"]["ID"] == car:
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

        for brand in brands:
            avg_brand_mpg[brand] = {"Brand": brand,
                                    "Car Count": 0,
                                    "Total MPG": 0,
                                    "Average MPG": 0}

        for x in cars:

            if x["Identification"]["Make"] in avg_brand_mpg:
                avg_brand_mpg[x["Identification"]["Make"]]["Car Count"] += 1
                avg_brand_mpg[x["Identification"]["Make"]]["Total MPG"] += (x["Fuel Information"]["City mpg"] + x["Fuel Information"]["Highway mpg"]) / 2
                avg_brand_mpg[x["Identification"]["Make"]]["Average MPG"] = round(avg_brand_mpg[x["Identification"]["Make"]]["Total MPG"] / avg_brand_mpg[x["Identification"]["Make"]]["Car Count"])

        return avg_brand_mpg



if __name__=="__main__":
    app.run(debug=False)