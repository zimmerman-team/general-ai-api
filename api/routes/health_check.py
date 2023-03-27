from flask import Blueprint

from api.routes import util

bp = Blueprint('health_check', __name__, url_prefix='/health-check')


@bp.route('/', methods=['GET'])
def health_check():
    # Return a 200 OK response as JSON
    return util.json_return(200, 'OK')
