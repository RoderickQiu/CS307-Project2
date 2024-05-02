import os
from flask_cors import CORS

# App Initialization
from . import create_app  # from __init__ file

app = create_app(os.getenv("CONFIG_MODE"))
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def hello():
    return "Hello World!"


from .urls import *

if __name__ == "__main__":
    app.run()
