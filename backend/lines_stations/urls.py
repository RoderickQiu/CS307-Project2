from flask import request

from ..app import app
from .controllers import *


@app.route("/lines", methods=["GET", "POST"])
def list_create_lines():
    if request.method == "GET":
        return list_all_lines_controller()
    if request.method == "POST":
        return create_line_controller()
    else:
        return "Method is Not Allowed"


@app.route("/lines/<line_id>", methods=["GET", "PUT", "DELETE"])
def retrieve_update_destroy_lines(line_id):
    if request.method == "GET":
        return retrieve_line_controller(line_id)
    if request.method == "PUT":
        return update_line_controller(line_id)
    if request.method == "DELETE":
        return delete_line_controller(line_id)
    else:
        return "Method is Not Allowed"


@app.route("/stations", methods=["GET", "POST"])
def list_create_stations():
    if request.method == "GET":
        return list_all_stations_controller()
    if request.method == "POST":
        return create_station_controller()
    else:
        return "Method is Not Allowed"


@app.route("/stations/<station_id>", methods=["GET", "PUT", "DELETE"])
def retrieve_update_destroy_stations(station_id):
    if request.method == "GET":
        return retrieve_station_controller(station_id)
    if request.method == "PUT":
        return update_station_controller(station_id)
    if request.method == "DELETE":
        return delete_station_controller(station_id)
    else:
        return "Method is Not Allowed"


# To-do
# 3. Station and line:
# Place one or more stations at a specified location on a line.
# Remove a station from a line.
# 4. Search the name of the stations that are the n-th station ahead and the n-th station behind a
# specific station on a line.


@app.route("/lines/<line_id>/stations", methods=["GET"])
def list_create_stations_on_line(line_id):
    if request.method == "GET":
        return list_stations_on_line_controller(line_id)
    else:
        return "Method is Not Allowed"


@app.route("/lines/<line_id>/stations/<station_id>", methods=["DELETE", "POST", "GET"])
def remove_station_from_line(line_id, station_id):
    if request.method == "GET":
        return get_station_on_line_controller(line_id, station_id)
    if request.method == "DELETE":
        return delete_station_from_line_controller(line_id, station_id)
    if request.method == "POST":
        return add_station_to_line_controller(line_id, station_id)
    else:
        return "Method is Not Allowed"


@app.route("/lines/<line_id>/stations/<station_id>/n/<n>", methods=["GET"])
def get_n_station_on_line(line_id, station_id, n):
    if request.method == "GET":
        return get_n_station_on_line_controller(line_id, station_id, n)
    else:
        return "Method is Not Allowed"
