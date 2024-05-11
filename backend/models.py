from sqlalchemy import inspect
from sqlalchemy import event

from backend.app import db  # from __init__.py


class LineDetail(db.Model):
    __tablename__ = "line_details"
    line_id = db.Column(db.Integer, db.ForeignKey("lines.line_id"), primary_key=True)
    station_id = db.Column(
        db.Integer, db.ForeignKey("stations.station_id"), primary_key=True
    )
    line_num = db.Column(db.Integer, nullable=False)

    line = db.relationship("Line", back_populates="stations")
    station = db.relationship("Station", back_populates="lines")

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Line(db.Model):
    __tablename__ = "lines"
    line_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    line_name = db.Column(db.String(10), nullable=False)
    business_carriage = db.Column(db.Integer)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    intro = db.Column(db.Text)
    mileage = db.Column(db.String(10), nullable=False)
    color = db.Column(db.String(10), nullable=False)
    first_opening = db.Column(db.Date, nullable=False)
    url = db.Column(db.String(100), nullable=False)

    stations = db.relationship(
        "LineDetail", back_populates="line"
    )  # name used for back_populates

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @staticmethod
    def default_business_carriage(mapper, connection, target):
        if target.business_carriage is None:
            target.business_carriage = 0


event.listen(Line, "before_insert", Line.default_business_carriage)


class Station(db.Model):
    __tablename__ = "stations"
    station_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    english_name = db.Column(db.String(900), nullable=False)
    chinese_name = db.Column(db.String(900), nullable=False)
    district = db.Column(db.String(900), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    introduction = db.Column(db.Text)
    lines = db.relationship(
        "LineDetail", back_populates="station"
    )  # name used for back_populates

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @staticmethod
    def default_status(mapper, connection, target):
        if target.status is None:
            target.status = "opening"


event.listen(Station, "before_insert", Station.default_status)


class Users(db.Model):
    __tablename__ = "users"
    user_id_number = db.Column(
        db.String(18), primary_key=True, nullable=False, unique=True
    )
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(11))
    gender = db.Column(db.String(1))
    district = db.Column(db.String(18))

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class UserRides(db.Model):
    __tablename__ = "user_rides"
    ride_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.String(18), nullable=False)
    business_carriage = db.Column(db.Integer)
    on_the_ride = db.Column(db.Integer, nullable=False)
    from_station = db.Column(db.Integer, nullable=False)
    to_station = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    start_time = db.Column(db.String(255))
    end_time = db.Column(db.String(255))

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Cards(db.Model):
    __tablename__ = "cards"
    card_number = db.Column(
        db.String(10), primary_key=True, nullable=False, unique=True
    )
    money = db.Column(db.Float, nullable=False)
    create_time = db.Column(db.String(255))

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class CardRides(db.Model):
    __tablename__ = "card_rides"
    ride_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    card_id = db.Column(db.String(10), nullable=False)
    business_carriage = db.Column(db.Integer)
    on_the_ride = db.Column(db.Integer, nullable=False)
    from_station = db.Column(db.Integer, nullable=False)
    to_station = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    start_time = db.Column(db.String(255))
    end_time = db.Column(db.String(255))

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
