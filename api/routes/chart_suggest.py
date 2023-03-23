from flask import Blueprint, request
import pandas as pd

from api.services.chart_suggest.csv_file import suggest_chart_for_csv_file

bp = Blueprint('chart_suggest', __name__, url_prefix='/chart-suggest')


@bp.route('/csv-dataset', methods=['post'])
def chart_suggest_for_dataset():
    """
    The input is a CSV file.
    We process the CSV file and return a list of suggested charts.
    """
    if 'file' not in request.files:
        return {'code': 400, 'result': 'No file uploaded'}, 400

    csv_file = request.files['file']
    if csv_file.filename == '':
        return {'code': 400, 'result': 'Empty filename'}, 400

    if csv_file and csv_file.filename.endswith('.csv'):
        df = pd.read_csv(csv_file)
        res = suggest_chart_for_csv_file(df)
        return {'code': 200, 'result': res}, 200
    else:
        return {'code': 400, 'result': 'Uploaded file was not recognized as a CSV file'}, 400
