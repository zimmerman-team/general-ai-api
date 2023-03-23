from flask import Blueprint

bp = Blueprint('base_route', __name__)
BASE_REPSONSE = 'Welcome to the Zimmerman General AI API! Consult the documentation for the API endpoints.'


@bp.route('/', methods=['GET'])
def base_route():
    # Return a 200 OK response as JSON
    return {'code': 200, 'result': BASE_REPSONSE}, 200
