from sqlalchemy import inspect
from datetime import datetime
from flask_validator import ValidateEmail, ValidateString, ValidateCountry
from sqlalchemy.orm import validates

from .. import db  # from __init__.py


# SQL Datatype Objects => https://docs.sqlalchemy.org/en/14/core/types.html
class Stations(db.Model):
    station_id = db.Column(
        db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    english_name = db.Column(db.String(900), nullable=False)
    chinese_name = db.Column(db.String(900), nullable=False)
    district = db.Column(db.String(900), nullable=False)
    introduction = db.Column(db.Text)

    # How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522
    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
