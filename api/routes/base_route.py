from flask import Blueprint

from api.routes import util

bp = Blueprint('base_route', __name__)
BASE_REPSONSE = 'Welcome to the Zimmerman General AI API! Consult the documentation for the API endpoints.'


@bp.route('/', methods=['GET'])
def base_route():
    # Return a 200 OK response as JSON
    return util.json_return(200, BASE_REPSONSE)
