from flask import request

from ..app import app
from .controllers import (
    list_all_lines_controller,
    create_line_controller,
    retrieve_line_controller,
    update_line_controller,
    delete_line_controller,
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
