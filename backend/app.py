import os
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from gevent.pywsgi import WSGIServer
from gevent import monkey

monkey.patch_all()

from .config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_mode):
    app = Flask(__name__)
    app.config.from_object(config[config_mode])
    db.init_app(app)
    migrate.init_app(app, db)

    return app

app = create_app(os.getenv("CONFIG_MODE"))
cors = CORS(app, resources={r"/*": {"origins": "*"}})

from .urls import *

@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(processes=True)
