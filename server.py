"""
Flask web app that exposes a restful API to obs

"""
import datetime
import uuid

import flask.json
from flask import Flask, request, jsonify, _request_ctx_stack, g
import redis

from jwtauth import requires_auth, handle_error


app = Flask(__name__)

# dummy data var in place of db
obs = [
    {
        'uid': uuid.uuid4(),
        'datetime': datetime.datetime(2016, 10, 11, 20, 7, 24),
        'weight': 76.67
    },
    {
        'uid': uuid.uuid4(),
        'datetime': datetime.datetime(2016, 10, 11, 20, 7, 24),
        'weight': 75.1
    }
]


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = redis.Redis(host='127.0.0.1',
                                port=6379,
                                db=0)
    return db


def init_db():
    db = get_db()
    for ob in obs:
        db.set(ob['uid'], flask.json.dumps(ob))


@app.cli.command('init_db')
def init_db_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


# Controllers API
@app.route("/ping")
def ping():
    return "All good. You don't need to be authenticated to call this"


@app.route("/secured/ping")
@requires_auth
def securedPing():
    return "All good. You only get this message if you're authenticated"


@app.route('/v1/obs/', methods=['GET'])
def get_obs():
    db = get_db()
    obs = [flask.json.loads(db.get(key)) for key in db.keys()]
    return jsonify(dict(obs=obs))


@app.route('/v1/obs/<uid>', methods=['GET'])
def get_ob(uid):
    ob = get_db().get(uid)
    if ob is None:
        return handle_error({'code': 'unknown_resource',
                             'description': 'Specified id is not recognised'},
                            404)
    ob = flask.json.loads(ob)
    return jsonify({'obs': ob})


@app.route('/v1/obs/', methods=['POST'])
def create_ob():
    if not request.json or not 'weight' in request.json:
        return handle_error({'code': 'ilformed_payload',
                             'description': 'Missing weight from observation'},
                            400)
    ob = {
        'uid': uuid.uuid4(),
        #'datetime': request.json['datetime'],
        'weight': request.json['weight']  # Add validation on insert
    }
    obs.append(ob)
    return jsonify({'obs': ob}), 201


if __name__ == "__main__":
    app.run()
