from flask import request, jsonify

from .. import db
from .models import Lines

# Query Object Methods => https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query
# Session Object Methods => https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session
# How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522


def list_all_lines_controller():
    lines = Lines.query.all()
    response = []
    for line in lines:
        response.append(line.toDict())
    return jsonify(response)


def create_line_controller():
    request_form = request.form.to_dict()

    new_line = Lines(
        start_time=request_form["start_time"],
        end_time=request_form["end_time"],
        intro=request_form["intro"],
        mileage=request_form["mileage"],
        color=request_form["color"],
        first_opening=request_form["first_opening"],
        url=request_form["url"],
    )
    db.session.add(new_line)
    db.session.commit()

    response = Lines.query.get(id).toDict()
    return jsonify(response)


def retrieve_line_controller(line_id):
    response = Lines.query.get(line_id).toDict()
    return jsonify(response)


def update_line_controller(line_id):
    request_form = request.form.to_dict()
    line = Lines.query.get(line_id)

    line.start_time = request_form["start_time"]
    line.end_time = request_form["end_time"]
    line.intro = request_form["intro"]
    line.mileage = request_form["mileage"]
    line.color = request_form["color"]
    line.first_opening = request_form["first_opening"]
    line.url = request_form["url"]

    db.session.commit()

    response = Lines.query.get(line_id).toDict()
    return jsonify(response)


def delete_line_controller(line_id):
    Lines.query.filter_by(id=line_id).delete()
    db.session.commit()

    return ('Line with Id "{}" deleted successfully!').format(line_id)
