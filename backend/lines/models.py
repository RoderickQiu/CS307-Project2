from sqlalchemy import inspect
from datetime import datetime
from flask_validator import ValidateEmail, ValidateString, ValidateCountry
from sqlalchemy.orm import validates

from .. import db  # from __init__.py


# SQL Datatype Objects => https://docs.sqlalchemy.org/en/14/core/types.html
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

    # How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522
    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
