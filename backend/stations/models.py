from sqlalchemy import inspect

from .. import db  # from __init__.py


class Stations(db.Model):
    station_id = db.Column(
        db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    english_name = db.Column(db.String(900), nullable=False)
    chinese_name = db.Column(db.String(900), nullable=False)
    district = db.Column(db.String(900), nullable=False)
    introduction = db.Column(db.Text)

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
