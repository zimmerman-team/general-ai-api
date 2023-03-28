import pandas as pd
from flask import Blueprint, request

from api.routes import util
from api.services.chart_suggest.chart_fields_from_data import suggest_chart_fields_from_data
from api.services.chart_suggest.chart_for_csv_file import suggest_chart_for_csv_file
from api.services.chart_suggest.chart_for_csv_file_with_context import suggest_chart_for_csv_file_with_context

bp = Blueprint('chart_suggest', __name__, url_prefix='/chart-suggest')


@bp.route('/csv-dataset', methods=['post'])
def chart_suggest_for_dataset():
    """
    The input is a CSV file.
    We process the CSV file and return a list of suggested charts.
    """
    # ret can be a json return object or the content of the provided csv file
    file_ok, ret = util.check_file(request, '.csv')
    if not file_ok:
        return ret

    df = pd.read_csv(ret)
    code, res = suggest_chart_for_csv_file(df)
    return util.json_return(code, res)


@bp.route('/chart-from-data', methods=['post'])
def chart_suggest_for_chart_from_data():
    """
    The input is a chart and data.
    We suggest fields for a chart based on the provided data.
    """
    file_ok, ret = util.check_file(request, '.csv')
    if not file_ok:
        return ret
    df = pd.read_csv(ret)

    chart = request.form['chart']
    code, res = suggest_chart_fields_from_data(df, chart)

    return util.json_return(code, res)


@bp.route('/csv-dataset-with-context', methods=['post'])
def chart_suggest_for_dataset_with_context():
    """
    The input is a chart and data.
    We suggest fields for a chart based on the provided data.
    """
    file_ok, ret = util.check_file(request, '.csv')
    if not file_ok:
        return ret
    df = pd.read_csv(ret)
    code, res = suggest_chart_for_csv_file_with_context(df)

    return util.json_return(code, res)
