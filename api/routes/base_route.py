from flask import Blueprint, Response

bp = Blueprint('base_route', __name__)
BASE_REPSONSE = 'Welcome to the Zimmerman General AI API! Consult the documentation for the API endpoints.'


@bp.route('/', methods=['GET'])
def base_route():
    # Return a 200 OK response as JSON
    return Response(BASE_REPSONSE, status=200, mimetype='text/plain')
