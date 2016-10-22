"""
Flask web app that exposes a restful API to obs

"""
import datetime
import uuid

from flask import Flask, request, jsonify, _request_ctx_stack

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
    return jsonify({'obs': obs})


@app.route('/v1/obs/<uid>', methods=['GET'])
def get_ob(uid):
    matching = [ob for ob in obs if str(ob['uid']) == uid]
    if not matching:
        return handle_error({'code': 'unknown_resource',
                             'description': 'Specified id is not recognised'},
                            404)
    if len(matching) != 1:
        return handle_error({'code': 'multiple_resources',
                             'description': 'Specified uid matches \
                                             multiple resources'},
                            400)
    return jsonify({'obs': matching[0]})


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
