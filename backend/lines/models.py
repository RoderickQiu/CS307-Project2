from sqlalchemy import inspect

from .. import db  # from __init__.py

LineDetails = db.Table(
    "Line_details",
    db.Column("line_id", db.Integer, db.ForeignKey("lines.line_id"), primary_key=True),
    db.Column(
        "station_id", db.Integer, db.ForeignKey("stations.station_id"), primary_key=True
    ),
    db.Column("line_num", db.Integer, nullable=False),
)


class Lines(db.Model):
    line_id = db.Column(
        db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    intro = db.Column(db.Text)
    mileage = db.Column(db.String(10), nullable=False)
    color = db.Column(db.String(10), nullable=False)
    first_opening = db.Column(db.Date, nullable=False)
    url = db.Column(db.String(100), nullable=False)

    line_detail = db.relationship("Stations", secondary=LineDetails, backref="lines")

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
