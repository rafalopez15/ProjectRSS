import os

from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/ProjectRss"

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    mongo.init_app(app)

    from . import feed
    app.register_blueprint(feed.bp)
    app.add_url_rule('/', endpoint='index')

    return app