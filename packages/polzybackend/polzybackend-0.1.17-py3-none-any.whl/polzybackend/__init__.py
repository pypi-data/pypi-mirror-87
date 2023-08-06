from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPTokenAuth
import os
from polzybackend.messenger import Messenger


# initialization
db = SQLAlchemy()
migrate = Migrate()
auth = HTTPTokenAuth(scheme='Bearer')
messenger = Messenger()


def create_app(config=None):
    # create application
    app = Flask(__name__)
    # set default config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', default = 'secret!key')
    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        default='sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'polzy.db'),
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(config)

    # policy store
    app.config['POLICIES'] = {}

    db.init_app(app)
    migrate.init_app(app, db)

    from polzybackend.authenticate import bp as bp_auth
    app.register_blueprint(bp_auth)

    from polzybackend.main import bp as bp_main
    app.register_blueprint(bp_main)

    from polzybackend.announce import bp as bp_announce
    app.register_blueprint(bp_announce)

    # -----------> DEBUG BLUEPRINT
    from polzybackend.debug import bp as bpDebug
    app.register_blueprint(bpDebug)

    return app



from polzybackend import models
