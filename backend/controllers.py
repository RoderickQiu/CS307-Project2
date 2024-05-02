from flask import request, jsonify

from . import db
from .models import Line, Station, LineDetail, Users, Cards, CardRides, UserRides


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
    lines = Line.query.all()
    max_line_id = max(line.line_id for line in lines) if lines else 0
    new_line_id = max_line_id + 1

    new_line = Line(
        line_id=new_line_id,
        line_name=request_form["line_name"],
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

    response = Line.query.get(new_line_id).toDict()
    return jsonify(response)


def retrieve_line_controller(line_id):
    line = Line.query.get(line_id)
    if line is None:
        return jsonify({"error": "Line with Id '{}' does not exist.".format(line_id)}), 404
    response = line.toDict()
    return jsonify(response)


def update_line_controller(line_id):
    request_form = request.form.to_dict()
    line = Line.query.get(line_id)

    line.line_name = request_form["line_name"]
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
    line = Line.query.get(line_id)
    if line is None:
        return jsonify({"error": "Line with Id '{}' does not exist.".format(line_id)}), 404

    Line.query.filter_by(line_id=line_id).delete()
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
    stations = Station.query.all()
    max_id = max(station.station_id for station in stations) if stations else 0
    new_id = max_id + 1
    new_station = Station(
        station_id=new_id,
        english_name=request_form["english_name"],
        chinese_name=request_form["chinese_name"],
        district=request_form["district"],
        introduction=request_form["introduction"],
    )
    db.session.add(new_station)
    db.session.commit()

    response = Station.query.get(new_id).toDict()
    return jsonify(response)


def retrieve_station_controller(station_id):
    station = Station.query.get(station_id)
    if station is None:
        return jsonify({"error": "Station with Id '{}' does not exist.".format(station_id)}), 404
    response = station.toDict()
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
    station = Station.query.get(station_id)
    if station is None:
        return jsonify({"error": "Station with Id '{}' does not exist.".format(station_id)}), 404

    Station.query.filter_by(station_id=station_id).delete()
    db.session.commit()
    return ('Station with Id "{}" deleted successfully!').format(station_id)


def delete_station_from_line_controller(line_id, station_id):
    line_detail = LineDetail.query.filter_by(
        line_id=line_id, station_id=station_id
    ).first()
    if line_detail is not None:
        # Update the line_num of the following stations
        following_stations = LineDetail.query.filter_by(line_id=line_id).filter(
            LineDetail.line_num > line_detail.line_num
        )
        for following_station in following_stations:
            following_station.line_num -= 1

        db.session.delete(line_detail)

        db.session.commit()
        return (
            'Station with Id "{}" removed from Line with Id "{}" successfully!'
        ).format(station_id, line_id)
    db.session.commit()

    return jsonify({"error": "Station with Id '{}' and Line with Id '{}' does not exist.".format(station_id, line_id)}), 404


def add_station_to_line_controller(line_id, station_id):
    request_form = request.form.to_dict()
    position = int(request_form["line_num"])

    line_detail = LineDetail.query.filter_by(
        line_id=line_id, station_id=station_id
    ).first()
    if line_detail is not None:
        return "Station already exists in the Line, abort!"
    else:
        # Update the line_num of the following stations
        following_stations = LineDetail.query.filter_by(line_id=line_id).filter(
            LineDetail.line_num >= position
        )
        for following_station in following_stations:
            following_station.line_num += 1

        # Add the new station to the line
        new_line_detail = LineDetail(
            line_id=line_id, station_id=station_id, line_num=position
        )
        db.session.add(new_line_detail)

    db.session.commit()

    response = (
        LineDetail.query.filter_by(line_id=line_id, station_id=station_id)
        .first()
        .toDict()
    )
    return jsonify(response)


def list_stations_on_line_controller(line_id):
    line_details = (
        LineDetail.query.filter_by(line_id=line_id).order_by(LineDetail.line_num).all()
    )
    response = []
    for line_detail in line_details:
        response.append(line_detail.toDict())
    return jsonify(response)


def get_station_on_line_controller(line_id, station_id):
    line_detail = LineDetail.query.filter_by(
        line_id=line_id, station_id=station_id
    ).first()
    if line_detail is not None:
        return jsonify(line_detail.toDict())
    else:
        return "Station not found in the Line!"


def get_n_station_on_line_controller(line_id, station_id, n):
    line_detail = LineDetail.query.filter_by(
        line_id=line_id, station_id=station_id
    ).first()
    if line_detail is not None:
        n_station = (
            LineDetail.query.filter_by(line_id=line_id)
            .filter(LineDetail.line_num == line_detail.line_num + int(n))
            .first()
        )
        if n_station is not None:
            return jsonify(n_station.toDict())
        else:
            return "Station not found in the Line!"
    else:
        return "Station not found in the Line!"
    
def list_all_users_controller():
    users = Users.query.all()
    response = []
    for user in users:
        response.append(user.toDict())
    return jsonify(response)

def create_user_controller():
    request_form = request.form.to_dict()
    new_user = Users(
        user_id_number=request_form["user_id_number"],
        name=request_form["name"],
        phone=request_form["phone"],
        gender=request_form["gender"],
        district=request_form["district"],
    )
    db.session.add(new_user)
    db.session.commit()

    response = Users.query.get(request_form["user_id_number"]).toDict()
    return jsonify(response)

def list_all_cards_controller():
    cards = Cards.query.all()
    response = []
    for card in cards:
        response.append(card.toDict())
    return jsonify(response)

def create_card_controller():
    request_form = request.form.to_dict()
    new_card = Cards(
        card_number=request_form["card_number"],
        money=request_form["money"],
        create_time=request_form["create_time"],
    )
    db.session.add(new_card)
    db.session.commit()

    response = Cards.query.get(request_form["card_number"]).toDict()
    return jsonify(response)

def list_all_card_rides_controller():
    card_rides = CardRides.query.all()
    response = []
    for card_ride in card_rides:
        response.append(card_ride.toDict())
    return jsonify(response)

def create_card_ride_controller():
    request_form = request.form.to_dict()
    card_rides = CardRides.query.all()
    max_ride_id = max(card_ride.ride_id for card_ride in card_rides) if card_rides else 0
    new_ride_id = max_ride_id + 1
    new_card_ride = CardRides(
        ride_id=new_ride_id,
        card_id=request_form["card_id"],
        on_the_ride=0,
        from_station=request_form["from_station"],
        to_station=request_form["from_station"],
        price=0,
        start_time=request_form["start_time"],
        end_time=request_form["start_time"],
    )
    db.session.add(new_card_ride)
    db.session.commit()

    response = CardRides.query.get(new_ride_id).toDict()
    return jsonify(response)

def list_all_user_rides_controller():
    user_rides = UserRides.query.all()
    response = []
    for user_ride in user_rides:
        response.append(user_ride.toDict())
    return jsonify(response)

def create_user_ride_controller():
    request_form = request.form.to_dict()
    user_rides = UserRides.query.all()
    max_ride_id = max(user_ride.ride_id for user_ride in user_rides) if user_rides else 0
    new_ride_id = max_ride_id + 1
    new_user_ride = UserRides(
        ride_id=new_ride_id,
        user_id=request_form["user_id"],
        on_the_ride=0,
        from_station=request_form["from_station"],
        to_station=request_form["from_station"],
        price=0,
        start_time=request_form["start_time"],
        end_time=request_form["start_time"],
    )
    db.session.add(new_user_ride)
    db.session.commit()

    response = UserRides.query.get(new_ride_id).toDict()
    return jsonify(response)

def retrieve_card_ride_controller(ride_id):
    ride = CardRides.query.get(ride_id)
    if ride is None:
        return jsonify({"error": "Card Ride with Id '{}' does not exist.".format(ride_id)}), 404
    response = ride.toDict()
    return jsonify(response)

def retrieve_user_ride_controller(ride_id):
    ride = UserRides.query.get(ride_id)
    if ride is None:
        return jsonify({"error": "User Ride with Id '{}' does not exist.".format(ride_id)}), 404
    response = ride.toDict()
    return jsonify(response)

def delete_card_ride_controller(ride_id):
    card_ride = CardRides.query.get(ride_id)
    if card_ride is None:
        return jsonify({"error": "Card Ride with Id '{}' does not exist.".format(ride_id)}), 404

    CardRides.query.filter_by(ride_id=ride_id).delete()
    db.session.commit()
    return ('Card Ride with Id "{}" deleted successfully!').format(ride_id)

def delete_user_ride_controller(ride_id):
    user_ride = UserRides.query.get(ride_id)
    if user_ride is None:
        return jsonify({"error": "User Ride with Id '{}' does not exist.".format(ride_id)}), 404

    UserRides.query.filter_by(ride_id=ride_id).delete()
    db.session.commit()
    return ('User Ride with Id "{}" deleted successfully!').format(ride_id)

def update_card_ride_controller(ride_id):
    request_form = request.form.to_dict()
    ride = CardRides.query.get(ride_id)

    ride.on_the_ride = 1
    ride.to_station = request_form["to_station"]
    ride.price = request_form["price"]
    ride.end_time = request_form["end_time"]

    db.session.commit()

    response = CardRides.query.get(ride_id).toDict()
    return jsonify(response)

def update_user_ride_controller(ride_id):
    request_form = request.form.to_dict()
    ride = UserRides.query.get(ride_id)
    ride.on_the_ride = 1
    ride.to_station = request_form["to_station"]
    ride.price = request_form["price"]
    ride.end_time = request_form["end_time"]

    db.session.commit()

    response = UserRides.query.get(ride_id).toDict()
    return jsonify(response)

def retrieve_online_person_controller():
    card_rides = CardRides.query.filter_by(on_the_ride=0).all()
    user_rides = UserRides.query.filter_by(on_the_ride=0).all()
    response = []
    for card_ride in card_rides:
        response.append(card_ride.toDict())
    for user_ride in user_rides:
        response.append(user_ride.toDict())
    return jsonify(response)