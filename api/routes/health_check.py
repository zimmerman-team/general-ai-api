from flask import Blueprint

bp = Blueprint('health_check', __name__, url_prefix='/health-check')


@bp.route('/', methods=['GET'])
def health_check():
    # Return a 200 OK response as JSON
    return {'code': 200, 'result': 'OK'}, 200
