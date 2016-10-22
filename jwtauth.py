"""
JWT based auth dectorators

"""

import jwt
import base64
import os

from functools import wraps
from flask import Flask, request, jsonify, _request_ctx_stack
from dotenv import Dotenv

env = None

try:
    env = Dotenv('./.env')
except IOError:
    env = os.environ

if env is not None:
    client_id = env["AUTH0_CLIENT_ID"]
    client_secret = env["AUTH0_CLIENT_SECRET"]


app = Flask(__name__)


# Format error response and append status code.
def handle_error(error, status_code):
    resp = jsonify(error)
    resp.status_code = status_code
    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return handle_error({'code': 'authorization_header_missing',
                                 'description': 'Authorization header is expected'},
                                401)

        parts = auth.split()
        print parts

        if parts[0].lower() != 'bearer':
            return handle_error({'code': 'invalid_header',
                                 'description': 'Authorization header must start with Bearer'},
                                401)
        elif len(parts) == 1:
            return handle_error({'code': 'invalid_header',
                                 'description': 'Token not found'},
                                401)
        elif len(parts) > 2:
            return handle_error({'code': 'invalid_header',
                                 'description': 'Authorization header must be Bearer + \s + token'},
                                401)

        token = parts[1]
        try:
            payload = jwt.decode(
                token,
                #key=client_secret,
                key=base64.b64decode(client_secret.replace("_", "/").replace("-", "+")),
                audience=client_id
            )
        except jwt.ExpiredSignature:
            return handle_error({'code': 'token_expired',
                                 'description': 'token is expired'},
                                401)
        except jwt.InvalidAudienceError:
            return handle_error({'code': 'invalid_audience',
                                 'description': 'incorrect audience, expected: ' + client_id},
                                401)
        except jwt.DecodeError:
            return handle_error({'code': 'token_invalid_signature',
                                 'description': 'token signature is invalid'},
                                401)
        except Exception:  # eek...
            return handle_error({'code': 'invalid_header',
                                 'description': 'Unable to parse authentication token.'},
                                400)

        _request_ctx_stack.top.current_user = user = payload
        return f(*args, **kwargs)
    return decorated

