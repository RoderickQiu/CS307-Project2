from sqlalchemy import inspect

from .. import db  # from __init__.py


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
    line_id = db.Column(
        db.Integer, primary_key=True, nullable=False, unique=True
    )
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    intro = db.Column(db.Text)
    mileage = db.Column(db.String(10), nullable=False)
    color = db.Column(db.String(10), nullable=False)
    first_opening = db.Column(db.Date, nullable=False)
    url = db.Column(db.String(100), nullable=False)

    stations = db.relationship("LineDetail", back_populates="line") # name used for back_populates

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Station(db.Model):
    __tablename__ = "stations"
    station_id = db.Column(
        db.Integer, primary_key=True, nullable=False, unique=True
    )
    english_name = db.Column(db.String(900), nullable=False)
    chinese_name = db.Column(db.String(900), nullable=False)
    district = db.Column(db.String(900), nullable=False)
    introduction = db.Column(db.Text)
    lines = db.relationship("LineDetail", back_populates="station") # name used for back_populates

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
