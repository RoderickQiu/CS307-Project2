from flask import request

from ..app import app
from .controllers import (
    list_all_lines_controller,
    create_line_controller,
    retrieve_line_controller,
    update_line_controller,
    delete_line_controller,
    list_all_stations_controller,
    create_station_controller,
    retrieve_station_controller,
    update_station_controller,
    delete_station_controller,
)


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
