from flask import (Flask, make_response, render_template,
                   request, jsonify, session, redirect)
from flask_sqlalchemy import SQLAlchemy
import json
from cardb import cardb
from cardb import types
import os
from functools import wraps


app = Flask(__name__)

interface = cardb.CarDB()

user = {
    "login": "Mechanik",
    "pass": "m3ch4n1k"
}


@app.route("/")
def home():
    return "Hello World"


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('username'):
            return redirect("login")
        return f(*args, **kwargs)
    return decorated


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.authorization and request.authorization.username == user[
                "login"] and request.authorization.password == user["pass"]:
            session['username'] = request.authorization.username
            resp = redirect('/cars')
            return resp
        return make_response(
            'not verified!', 401, {
                'WWW-Authenticate': 'Basic realm="Login Required"'})
    else:
        return "To log in, please use RESTer/POSTman and choose POST request method"


@app.route("/logout", methods=["POST"])
@auth_required
def logout():
    resp = redirect("/")
    session.pop('username', None)
    return resp


@app.route("/cars", methods=["GET", "POST", "PATCH", "DELETE"])
@auth_required
def my_cars(**filters):
    if request.method == "GET":
        return show_cars()
    elif request.method == "POST":
        return add_car()
    elif request.method == "DELETE":
        return delete_car()
    elif request.method == "PATCH":
        return update_car()


def show_cars():
    fil = list(dict(request.args).items())
    inf = request.args.get("info")
    if inf is None:
        if len(fil) == 0:
            result = interface.query_cars(filters=[])
            if len(result) > 0:
                r = [r.jsonize() for r in result]
                return jsonify(r)
            else:
                return "No cars in database"

        else:
            result = interface.query_cars(filters=fil)
            if None not in result:
                r = [r.jsonize() for r in result]
                return jsonify(r)
            else:
                return "Not found"
    else:
        result = interface.query_cars(filters=inf)
        if len(result) > 0:
            r = [r.jsonize() for r in result]
            return jsonify(r)
        else:
            return "No such car"


def add_car():
    data = request.get_json()
    brand = data.get("brand")
    model = data.get("model")
    info = data.get("info")
    interface.create_car(brand, model, **info)
    return "ok"


def delete_car(**filters):
    car_id = request.args.get("id")
    return interface.delete_car(car_id)


def update_car(**filters):
    data = request.get_json()
    identifier = request.args.get("id")
    return interface.update_car(identifier, data)


@app.route("/brands", methods=["GET", "POST", "DELETE"])
@auth_required
def my_brands(**filters):
    if request.method == "GET":
        return show_brands(**filters)
    elif request.method == "POST":
        return add_brand()
    elif request.method == "DELETE":
        return delete_brand()


def show_brands(**filters):
    filts = dict(request.args)
    filts = list(filts.items())
    if filts == []:
        res = interface.query_brands(filters=())
        if len(res) > 0:
            r = [r.jsonize() for r in res]
            return jsonify(r)
        else:
            return "No brands in database"
    else:
        filtr = list(filts[0])
        val = filtr[1][0]
        filts = [filtr[0], val]
        filters = tuple(filts)
        res = interface.query_brands(filters=filters)
        if isinstance(res, list) and isinstance(res[0], types.Brand):
            r = [r.jsonize() for r in res]
            return jsonify(r)
        else:
            return "No such brand"


def add_brand():
    data = request.get_json()
    name = data.get("name")
    brand = types.Brand()
    interface.create_brand(name)
    return "OK"


def delete_brand():
    brand_id = request.args.get("id")
    return interface.delete_brand(brand_id)


def update_brand():
    data = request.get_json()
    identifier = request.args.get("id")
    if identifier is not None:
        interface.update_brand(identifier, data)
        return "ok"
    else:
        return "Not found"


app.secret_key = "so_very_secret_key_so"

if __name__ == '__main__':
    app.run(debug=True)
