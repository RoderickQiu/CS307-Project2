from flask import request, jsonify
from sqlalchemy import func, Integer, text, DateTime
from datetime import datetime
from backend.app import db
from backend.app import app
from .models import Line, Station, LineDetail, Users, Cards, CardRides, UserRides


# Query Object Methods => https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query
# Session Object Methods => https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session
# How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522


def list_all_lines_controller():
    lines = Line.query.order_by(Line.line_id).all()
    response = []
    for line in lines:
        response.append(line.toDict())
    return jsonify(response)


def create_line_controller():
    request_form = request.form.to_dict()
    lines = Line.query.all()
    max_line_id = max(line.line_id for line in lines) if lines else 0
    new_line_id = max_line_id + 1
    business_carriage = request_form.get("business_carriage", 0)
    new_line = Line(
        line_id=new_line_id,
        line_name=request_form["line_name"],
        business_carriage=business_carriage,
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
        return (
            jsonify({"error": "Line with Id '{}' does not exist.".format(line_id)}),
            404,
        )
    response = line.toDict()
    return jsonify(response)


def update_line_controller(line_id):
    request_form = request.form.to_dict()
    line = Line.query.get(line_id)
    business_carriage = request_form.get("business_carriage", 0)
    line.line_name = request_form["line_name"]
    line.business_carriage = business_carriage
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
        return (
            jsonify({"error": "Line with Id '{}' does not exist.".format(line_id)}),
            404,
        )

    Line.query.filter_by(line_id=line_id).delete()
    db.session.commit()
    return ('Line with Id "{}" deleted successfully!').format(line_id)


def list_all_stations_controller():
    elem_per_page = int(request.args.get("elem_per_page", 10))
    page = int(
        request.args.get("page", 1)
    )  # for GET, use request.args instead of request.form
    offset = (page - 1) * elem_per_page
    stations = Station.query.order_by(Station.station_id).all()
    response = []
    for station in stations[offset : offset + elem_per_page]:
        response.append(station.toDict())
    return jsonify(
        {
            "page": page,
            "total": len(stations),
            "result": response,
        }
    )


def create_station_controller():
    request_form = request.form.to_dict()
    stations = Station.query.all()
    max_id = max(station.station_id for station in stations) if stations else 0
    new_id = max_id + 1
    status = request_form.get("status", "opening")
    new_station = Station(
        station_id=new_id,
        english_name=request_form["english_name"],
        chinese_name=request_form["chinese_name"],
        district=request_form["district"],
        status=status,
        introduction=request_form["introduction"],
    )
    db.session.add(new_station)
    db.session.commit()

    response = Station.query.get(new_id).toDict()
    return jsonify(response)


def retrieve_station_controller(station_id):
    station = Station.query.get(station_id)
    if station is None:
        return (
            jsonify(
                {"error": "Station with Id '{}' does not exist.".format(station_id)}
            ),
            404,
        )
    response = station.toDict()
    return jsonify(response)


def update_station_controller(station_id):
    request_form = request.form.to_dict()
    station = Station.query.get(station_id)
    status = request_form.get("status", "opening")
    station.english_name = request_form["english_name"]
    station.chinese_name = request_form["chinese_name"]
    station.district = request_form["district"]
    station.status = status
    station.introduction = request_form["introduction"]
    print(request_form)
    db.session.commit()

    response = Station.query.get(station_id).toDict()
    return jsonify(response)


def delete_station_controller(station_id):
    station = Station.query.get(station_id)
    if station is None:
        return (
            jsonify(
                {"error": "Station with Id '{}' does not exist.".format(station_id)}
            ),
            404,
        )

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

    return (
        jsonify(
            {
                "error": "Station with Id '{}' and Line with Id '{}' does not exist.".format(
                    station_id, line_id
                )
            }
        ),
        404,
    )


def add_multiple_stations_to_line_controller(line_id, station_ids):
    request_form = request.form.to_dict()
    position = int(request_form["line_num"])

    for station_id in station_ids:
        line_detail = LineDetail.query.filter_by(
            line_id=line_id, station_id=station_id
        ).first()
        if line_detail is not None:
            return (
                jsonify({"error": "Station already exists in the Line, abort!"}),
                400,
            )

    # Update the line_num of the following stations
    following_stations = LineDetail.query.filter_by(line_id=line_id).filter(
        LineDetail.line_num >= position
    )
    for following_station in following_stations:
        following_station.line_num += len(station_ids)

    # Add the new stations to the line
    for station_id in station_ids:
        new_line_detail = LineDetail(
            line_id=line_id, station_id=station_id, line_num=position
        )
        db.session.add(new_line_detail)
        position += 1

    db.session.commit()

    response = []
    for station_id in station_ids:
        response.append(
            LineDetail.query.filter_by(line_id=line_id, station_id=station_id)
            .first()
            .toDict()
        )
    return jsonify(response)


def add_station_to_line_controller(line_id, station_id):
    request_form = request.form.to_dict()
    position = int(request_form["line_num"])

    line_detail = LineDetail.query.filter_by(
        line_id=line_id, station_id=station_id
    ).first()
    if line_detail is not None:
        return (
            jsonify({"error": "Station already exists in the Line, abort!"}),
            400,
        )
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
        station = Station.query.get(line_detail.station_id)
        dict = station.toDict()
        dict["line_num"] = line_detail.line_num
        response.append(dict)

    response = sorted(response, key=lambda x: x["line_num"])
    return jsonify(response)


def get_station_on_line_controller(line_id, station_id):
    line_detail = LineDetail.query.filter_by(
        line_id=line_id, station_id=station_id
    ).first()
    if line_detail is not None:
        return jsonify(line_detail.toDict())
    else:
        return (
            jsonify({"error": "Station not found on line!"}),
            404,
        )


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
            return (
                jsonify({"error": "Station not found on line!"}),
                404,
            )
    else:
        return (
            jsonify({"error": "Station not found on line!"}),
            404,
        )


def list_all_users_controller():
    elem_per_page = int(request.args.get("elem_per_page", 10))
    page = int(
        request.args.get("page", 1)
    )  # for GET, use request.args instead of request.form
    offset = (page - 1) * elem_per_page
    users = Users.query.all()
    response = []
    for user in users[offset : offset + elem_per_page]:
        response.append(user.toDict())
    return jsonify(
        {
            "page": page,
            "total": len(users),
            "result": response,
        }
    )


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
    elem_per_page = int(request.args.get("elem_per_page", 10))
    page = int(
        request.args.get("page", 1)
    )  # for GET, use request.args instead of request.form
    offset = (page - 1) * elem_per_page
    cards = Cards.query.all()
    response = []

    for card in cards[offset : offset + elem_per_page]:
        response.append(card.toDict())

    return jsonify(
        {
            "page": page,
            "total": len(cards),
            "result": response,
        }
    )


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
    max_ride_id = (
        max(card_ride.ride_id for card_ride in card_rides) if card_rides else 0
    )
    new_ride_id = max_ride_id + 1
    new_card_ride = CardRides(
        ride_id=new_ride_id,
        card_id=request_form["card_id"],
        business_carriage=request_form["business_carriage"],
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
    max_ride_id = (
        max(user_ride.ride_id for user_ride in user_rides) if user_rides else 0
    )
    Current_From_Station = Station.query.filter_by(
        station_id=request_form["from_station"]
    ).first()
    if Current_From_Station.status != "opening":
        return jsonify({"error": "The station is not opening."}), 404
    new_ride_id = max_ride_id + 1
    new_user_ride = UserRides(
        ride_id=new_ride_id,
        user_id=request_form["user_id"],
        business_carriage=request_form["business_carriage"],
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
        return (
            jsonify(
                {"error": "Card Ride with Id '{}' does not exist.".format(ride_id)}
            ),
            404,
        )
    response = ride.toDict()
    return jsonify(response)


def retrieve_user_ride_controller(ride_id):
    ride = UserRides.query.get(ride_id)
    if ride is None:
        return (
            jsonify(
                {"error": "User Ride with Id '{}' does not exist.".format(ride_id)}
            ),
            404,
        )
    response = ride.toDict()
    return jsonify(response)


def delete_card_ride_controller(ride_id):
    card_ride = CardRides.query.get(ride_id)
    if card_ride is None:
        return (
            jsonify(
                {"error": "Card Ride with Id '{}' does not exist.".format(ride_id)}
            ),
            404,
        )

    CardRides.query.filter_by(ride_id=ride_id).delete()
    db.session.commit()
    return ('Card Ride with Id "{}" deleted successfully!').format(ride_id)


def delete_user_ride_controller(ride_id):
    user_ride = UserRides.query.get(ride_id)
    if user_ride is None:
        return (
            jsonify(
                {"error": "User Ride with Id '{}' does not exist.".format(ride_id)}
            ),
            404,
        )

    UserRides.query.filter_by(ride_id=ride_id).delete()
    db.session.commit()
    return ('User Ride with Id "{}" deleted successfully!').format(ride_id)


def find(from_station, to_station):
    with open("../data_process/data.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split(",")
        if parts[2] == from_station and parts[3] == to_station:
            return int(parts[4])

    return jsonify({"error": "No matching route found."}), 404


def update_card_ride_controller(ride_id):
    request_form = request.form.to_dict()
    ride = CardRides.query.get(ride_id)

    from_station_id = ride.from_station
    to_station_id = request_form["to_station"]
    from_station = Station.query.get(from_station_id)
    to_station = Station.query.get(to_station_id)
    if from_station is None or to_station is None:
        return jsonify({"error": "Station with given id does not exist."}), 404
    from_station_name = from_station.chinese_name
    to_station_name = to_station.chinese_name

    price = find(from_station_name, to_station_name)
    if ride.business_carriage == 1:
        price *= 2
    ride.on_the_ride = 1
    ride.to_station = request_form["to_station"]
    ride.price = price
    ride.end_time = request_form["end_time"]

    db.session.commit()

    response = CardRides.query.get(ride_id).toDict()
    return jsonify(response)


def update_user_ride_controller(ride_id):
    request_form = request.form.to_dict()
    ride = UserRides.query.get(ride_id)

    from_station_id = ride.from_station
    to_station_id = request_form["to_station"]
    from_station = Station.query.get(from_station_id)
    to_station = Station.query.get(to_station_id)
    if from_station is None or to_station is None:
        return jsonify({"error": "Station with given id does not exist."}), 404
    from_station_name = from_station.chinese_name
    to_station_name = to_station.chinese_name

    price = find(from_station_name, to_station_name)
    if ride.business_carriage == 1:
        price *= 2
    ride.on_the_ride = 1
    ride.to_station = request_form["to_station"]
    ride.price = price
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


def retrieve_card_rides_controller(card_number):
    card_rides = CardRides.query.filter_by(card_id=card_number).all()
    response = []
    for card_ride in card_rides:
        response.append(card_ride.toDict())
    return jsonify(response)


def retrieve_user_rides_controller(user_id):
    user_rides = UserRides.query.filter_by(user_id=user_id).all()
    response = []
    for user_ride in user_rides:
        response.append(user_ride.toDict())
    return jsonify(response)


def query_user_controller():
    request_form = request.form.to_dict()
    query = UserRides.query

    if "business_carriage" in request_form:
        query = query.filter(
            UserRides.business_carriage == request_form["business_carriage"]
        )

    if "from_station" in request_form:
        query = query.filter(UserRides.from_station == request_form["from_station"])

    if "to_station" in request_form:
        query = query.filter(UserRides.to_station == request_form["to_station"])

    if "user_id" in request_form:
        query = query.filter(UserRides.user_id == request_form["user_id"])

    if "on_the_ride" in request_form:
        query = query.filter(UserRides.on_the_ride == request_form["on_the_ride"])

    if "price" in request_form:
        query = query.filter(UserRides.price == request_form["price"])

    if "time" in request_form:
        time = datetime.strptime(request_form["time"], "%Y-%m-%dT%H:%M:%S")
        query = query.filter(
            func.cast(UserRides.start_time, DateTime) <= time,
            func.cast(UserRides.end_time, DateTime) >= time,
        )

    user_rides = query.all()
    response = []
    for user_ride in user_rides:
        response.append(user_ride.toDict())
    if not response:
        return jsonify({"error": "No matching user ride found."}), 404
    return jsonify(response)


def query_card_controller():
    request_form = request.form.to_dict()
    query = CardRides.query

    print(request_form)

    if "business_carriage" in request_form:
        query = query.filter(
            CardRides.business_carriage == request_form["business_carriage"]
        )

    if "from_station" in request_form:
        query = query.filter(CardRides.from_station == request_form["from_station"])

    if "to_station" in request_form:
        query = query.filter(CardRides.to_station == request_form["to_station"])

    if "card_id" in request_form:
        query = query.filter(CardRides.card_id == request_form["card_id"])

    if "on_the_ride" in request_form:
        query = query.filter(CardRides.on_the_ride == request_form["on_the_ride"])

    if "price" in request_form:
        query = query.filter(CardRides.price == request_form["price"])

    if "time" in request_form:
        time = datetime.strptime(request_form["time"], "%Y-%m-%dT%H:%M:%S")
        query = query.filter(
            func.cast(CardRides.start_time, DateTime) <= time,
            func.cast(CardRides.end_time, DateTime) >= time,
        )

    card_rides = query.all()
    response = []
    for card in card_rides:
        response.append(card.toDict())
    if not response:
        return jsonify({"error": "No matching card found."}), 404
    return jsonify(response)


def read_user_read_controller():
    user_rides = UserRides.query.all()
    response = []
    for user_ride in user_rides:
        response.append(user_ride.toDict())
    return jsonify(response)


def read_user_write_controller():
    with app.read_engine.connect() as conn:
        stmt = text(
            "INSERT INTO lines (line_id, line_name, business_carriage, start_time, end_time, intro, mileage, color, first_opening, url) VALUES (:line_id, :line_name, :business_carriage, :start_time, :end_time, :intro, :mileage, :color, :first_opening, :url)"
        )
        params = {
            "line_id": 17,
            "line_name": "100号线",
            "business_carriage": 0,
            "start_time": "06:00",
            "end_time": "23:59",
            "intro": "100号线",
            "mileage": "100",
            "color": "red",
            "first_opening": "2021-01-01",
            "url": "https://www.baidu.com",
        }
        conn.execute(stmt, params)
        return "Success", 201


def write_user_read_controller():
    with app.write_engine.connect() as conn:
        stmt = text("SELECT * FROM lines")
        result = conn.execute(stmt)
        response = []
        for row in result:
            response.append(dict(row))
        return jsonify(response)


def write_user_write_controller():
    with app.write_engine.connect() as conn:
        stmt = text(
            "INSERT INTO lines (line_id, line_name, business_carriage, start_time, end_time, intro, mileage, color, first_opening, url) VALUES (:line_id, :line_name, :business_carriage, :start_time, :end_time, :intro, :mileage, :color, :first_opening, :url)"
        )
        params = {
            "line_id": 17,
            "line_name": "100号线",
            "business_carriage": 0,
            "start_time": "06:00",
            "end_time": "23:59",
            "intro": "100号线",
            "mileage": "100",
            "color": "red",
            "first_opening": "2021-01-01",
            "url": "https://www.baidu.com",
        }
        conn.execute(stmt, params)
        return "Success", 201
