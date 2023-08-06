from . import bp
from polzybackend import messenger
from polzybackend.models import User
from flask import jsonify
import json


# toast debugging route
@bp.route('/ping')
def ping():
    #msg = messenger.format_sse(data='ping', event='fasifu')
    data = {
        'text': 'Fasifu message!',
        #'variant': 'success',
        #'anchorOrigin': {
        #    'vertical': 'top',
        #    'horizontal': 'left',
        #},
        #'autoHideDuration': 2000,
    }
    msg = f"data: {json.dumps(data)}\n\n"
    messenger.announce(msg=msg)
    return {}, 200


# returns all available users
@bp.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([u.email for u in users]), 200
