from flask import request

from .app import app
from .controllers import *


@app.route("/lines", methods=["GET", "POST"])  # /lines
def list_create_lines():
    if request.method == "GET":
        return list_all_lines_controller()
    if request.method == "POST":
        return create_line_controller()
    else:
        return "Method is Not Allowed"


@app.route("/lines/<line_id>", methods=["GET", "PUT", "DELETE"])  # /lines/1
def retrieve_update_destroy_lines(line_id):
    if request.method == "GET":
        return retrieve_line_controller(line_id)
    if request.method == "PUT":
        return update_line_controller(line_id)
    if request.method == "DELETE":
        return delete_line_controller(line_id)
    else:
        return "Method is Not Allowed"


@app.route("/stations", methods=["GET", "POST"])  # /stations
def list_create_stations():
    if request.method == "GET":
        return list_all_stations_controller()
    if request.method == "POST":
        return create_station_controller()
    else:
        return "Method is Not Allowed"


@app.route("/stations/<station_id>", methods=["GET", "PUT", "DELETE"])  # /stations/1
def retrieve_update_destroy_stations(station_id):
    if request.method == "GET":
        return retrieve_station_controller(station_id)
    if request.method == "PUT":
        return update_station_controller(station_id)
    if request.method == "DELETE":
        return delete_station_controller(station_id)
    else:
        return "Method is Not Allowed"


@app.route("/lines/<line_id>/stations", methods=["GET"])  # /lines/1/stations
def list_create_stations_on_line(line_id):
    if request.method == "GET":
        return list_stations_on_line_controller(line_id)
    else:
        return "Method is Not Allowed"


@app.route(
    "/lines/<line_id>/stations/<station_id>", methods=["DELETE", "POST", "GET"]
)  # /lines/1/stations/1
def remove_station_from_line(line_id, station_id):
    if request.method == "GET":
        return get_station_on_line_controller(line_id, station_id)
    if request.method == "DELETE":
        return delete_station_from_line_controller(line_id, station_id)
    if request.method == "POST":
        if station_id[0] == "[":
            station_id = station_id[1:-1]
            station_ids = station_id.split(",")
            return add_multiple_stations_to_line_controller(line_id, station_ids)
        else:
            return add_station_to_line_controller(line_id, station_id)
    else:
        return "Method is Not Allowed"


@app.route(
    "/lines/<line_id>/stations/<station_id>/n/<n>", methods=["GET"]
)  # /lines/1/stations/1/n/1
def get_n_station_on_line(line_id, station_id, n):
    if request.method == "GET":
        return get_n_station_on_line_controller(line_id, station_id, n)
    else:
        return "Method is Not Allowed"


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
@app.route("/users", methods=["GET", "POST"])  # /users
def list_create_users():
    if request.method == "GET":
        return list_all_users_controller()
    if request.method == "POST":
        return create_user_controller()
    else:
        return "Method is Not Allowed"


@app.route("/cards", methods=["GET", "POST"])  # /cards
def list_create_cards():
    if request.method == "GET":
        return list_all_cards_controller()
    if request.method == "POST":
        return create_card_controller()
    else:
        return "Method is Not Allowed"


@app.route("/card_rides", methods=["GET", "POST"])  # /card_ride
def list_create_card_rides():
    if request.method == "GET":
        return list_all_card_rides_controller()
    if request.method == "POST":
        return create_card_ride_controller()
    else:
        return "Method is Not Allowed"


@app.route("/user_rides", methods=["GET", "POST"])  # /user_ride
def list_create_user_rides():
    if request.method == "GET":
        return list_all_user_rides_controller()
    if request.method == "POST":
        return create_user_ride_controller()
    else:
        return "Method is Not Allowed"


@app.route("/card_rides/<ride_id>", methods=["GET", "DELETE", "PUT"])  # /card_ride/1
def retrieve_destroy_card_ride(ride_id):
    if request.method == "GET":
        return retrieve_card_ride_controller(ride_id)
    if request.method == "DELETE":
        return delete_card_ride_controller(ride_id)
    if request.method == "PUT":
        return update_card_ride_controller(ride_id)
    else:
        return "Method is Not Allowed"

@app.route("/card_rides/card/<card_number>", methods=["GET"])  # /card_ride/card/1
def retrieve_card_rides(card_number):
    if request.method == "GET":
        return retrieve_card_rides_controller(card_number)
    else:
        return "Method is Not Allowed"


@app.route("/user_rides/<ride_id>", methods=["GET", "DELETE", "PUT"])  # /user_ride/1
def retrieve_destroy_user_ride(ride_id):
    if request.method == "GET":
        return retrieve_user_ride_controller(ride_id)
    if request.method == "DELETE":
        return delete_user_ride_controller(ride_id)
    if request.method == "PUT":
        return update_user_ride_controller(ride_id)
    else:
        return "Method is Not Allowed"

@app.route("/user_rides/user/<user_id>", methods=["GET"])  # /user_ride/user/1
def retrieve_user_rides(user_id):
    if request.method == "GET":
        return retrieve_user_rides_controller(user_id)
    else:
        return "Method is Not Allowed"


@app.route("/online", methods=["GET"])
def retrieve_online_person():
    if request.method == "GET":
        return retrieve_online_person_controller()
    else:
        return "Method is Not Allowed"
    
# Bonus---------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# 多参数搜索乘⻋记录功能
@app.route("/queryuser", methods=["POST"])  # /queryuser
def query():
    if request.method == "POST":
        return query_user_controller()
    else:
        return "Method is Not Allowed"
    
@app.route("/querycard", methods=["POST"])  # /querycard
def query_card():
    if request.method == "POST":
        return query_card_controller()
    else:
        return "Method is Not Allowed"
