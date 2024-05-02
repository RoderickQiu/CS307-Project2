from flask import request, jsonify

from .. import db
from .models import Stations

# Query Object Methods => https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query
# Session Object Methods => https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session
# How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522


def list_all_stations_controller():
    stations = Stations.query.all()
    response = []
    for station in stations:
        response.append(station.toDict())
    return jsonify(response)


def create_station_controller():
    request_form = request.form.to_dict()

    new_station = Stations(
        english_name=request_form["english_name"],
        chinese_name=request_form["chinese_name"],
        district=request_form["district"],
        introduction=request_form["introduction"],
    )
    db.session.add(new_station)
    db.session.commit()

    response = Stations.query.get(id).toDict()
    return jsonify(response)


def retrieve_station_controller(station_id):
    response = Stations.query.get(station_id).toDict()
    return jsonify(response)


def update_station_controller(station_id):
    request_form = request.form.to_dict()
    station = Stations.query.get(station_id)

    station.english_name = request_form["english_name"]
    station.chinese_name = request_form["chinese_name"]
    station.district = request_form["district"]
    station.introduction = request_form["introduction"]

    db.session.commit()

    response = Stations.query.get(station_id).toDict()
    return jsonify(response)


def delete_station_controller(station_id):
    Stations.query.filter_by(id=station_id).delete()
    db.session.commit()

    return ('Stations with Id "{}" deleted successfully!').format(station_id)
