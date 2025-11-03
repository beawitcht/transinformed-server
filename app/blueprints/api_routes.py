import requests
import os
import ast

from flask import Blueprint, request, abort

api_bp = Blueprint('api', __name__)

@api_bp.route("/api/pass-thru", methods=['GET'])
def the_routler():

    # hide allowed endpoints to prevent misuse
    allowed_endpoints = ast.literal_eval(os.getenv('ALLOWED_ENDPOINTS'))
    query = request.args.get('query')
    allowed = False

    for endpoint in allowed_endpoints:
        if query.startswith(endpoint):
            allowed = True

    if not allowed:
        abort(403)

    response = requests.get(query)

    if not response.status_code:
        abort(400)
    elif response.status_code != 200:
        abort(response.status_code)

    return response.json()
