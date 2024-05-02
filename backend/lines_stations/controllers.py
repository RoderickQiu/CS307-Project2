from flask import request, jsonify

from .. import db
from .models import Line, Station

# Query Object Methods => https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query
# Session Object Methods => https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session
# How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522


def list_all_lines_controller():
    lines = Line.query.all()
    response = []
    for line in lines:
        response.append(line.toDict())
    return jsonify(response)


def create_line_controller():
    request_form = request.form.to_dict()

    new_line = Line(
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

    response = Line.query.get(id).toDict()
    return jsonify(response)


def retrieve_line_controller(line_id):
    response = Line.query.get(line_id).toDict()
    return jsonify(response)


def update_line_controller(line_id):
    request_form = request.form.to_dict()
    line = Line.query.get(line_id)

    line.start_time = request_form["start_time"]
    line.end_time = request_form["end_time"]
    line.intro = request_form["intro"]
    line.mileage = request_form["mileage"]
    line.color = request_form["color"]
    line.first_opening = request_form["first_opening"]
    line.url = request_form["url"]

    db.session.commit()

    response = Line.query.get(line_id).toDict()
    return jsonify(response)


def delete_line_controller(line_id):
    Line.query.filter_by(id=line_id).delete()
    db.session.commit()

    return ('Line with Id "{}" deleted successfully!').format(line_id)


def list_all_stations_controller():
    stations = Station.query.all()
    response = []
    for station in stations:
        response.append(station.toDict())
    return jsonify(response)


def create_station_controller():
    request_form = request.form.to_dict()

    new_station = Station(
        english_name=request_form["english_name"],
        chinese_name=request_form["chinese_name"],
        district=request_form["district"],
        introduction=request_form["introduction"],
    )
    db.session.add(new_station)
    db.session.commit()

    response = Station.query.get(id).toDict()
    return jsonify(response)


def retrieve_station_controller(station_id):
    response = Station.query.get(station_id).toDict()
    return jsonify(response)


def update_station_controller(station_id):
    request_form = request.form.to_dict()
    station = Station.query.get(station_id)

    station.english_name = request_form["english_name"]
    station.chinese_name = request_form["chinese_name"]
    station.district = request_form["district"]
    station.introduction = request_form["introduction"]

    db.session.commit()

    response = Station.query.get(station_id).toDict()
    return jsonify(response)


def delete_station_controller(station_id):
    Station.query.filter_by(id=station_id).delete()
    db.session.commit()

    return ('Station with Id "{}" deleted successfully!').format(station_id)
