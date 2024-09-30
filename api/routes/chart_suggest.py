import json

import pandas as pd
from flask import Blueprint, request

from api.routes import util
from api.services.chart_suggest.ai_report_builder import ai_report_builder_chart_selector
from api.services.chart_suggest.chart_fields_from_data import suggest_chart_fields_from_data
from api.services.chart_suggest.chart_for_csv_file import suggest_chart_for_csv_file
from api.services.chart_suggest.chart_for_csv_file_with_context import suggest_chart_for_csv_file_with_context
from api.services.openai.assistants import create_chart_builder_assistant, create_iati_query_assistant

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


@bp.route('/ai-report-builder', methods=['post'])
def chart_suggest_with_chart_from_data():
    """
    The input is a chart and data.
    We suggest fields for a chart based on the provided data.
    """
    file_ok, ret = util.check_file(request, '.csv')
    if not file_ok:
        return ret
    df = pd.read_csv(ret)

    sc_code, sc_res = ai_report_builder_chart_selector(df)
    if sc_code != 200:
        return util.json_return(sc_code, sc_res)

    # Json parse sc_res
    sc_res = json.loads(sc_res)

    charts = []
    for chart in sc_res:
        code, res = suggest_chart_fields_from_data(df, chart)
        # update `res` to be a substring starting with the first { and ending with the last }
        res = res[res.find('{'):res.rfind('}')+1]
        if code != 200:
            return util.json_return(code, res)
        charts.append(res)
    return util.json_return(code, charts)


@bp.route('/ai-report-builder-from-existing', methods=['get'])
def chart_suggest_with_existing_source():
    """
    The input is a chart and data.
    We suggest fields for a chart based on the provided data.
    """
    file_ok, ret = util.check_and_load_existing_file(request)
    if not file_ok:
        return ret
    df = pd.DataFrame(ret)

    sc_code, sc_res = ai_report_builder_chart_selector(df)
    if sc_code != 200:
        return util.json_return(sc_code, sc_res)
    sc_res = sc_res[sc_res.find('['):sc_res.rfind(']')+1]
    # Json parse sc_res
    sc_res = json.loads(sc_res)

    charts = []
    for chart in sc_res:
        if chart == 'line':
            chart = 'linechart'
        if chart == 'bar':
            chart = 'barchart'
        if chart == 'scatterplot':
            chart = 'scatterchart'
        code, res = suggest_chart_fields_from_data(df, chart)
        # update `res` to be a substring starting with the first { and ending with the last }
        res = res[res.find('{'):res.rfind('}')+1]
        if code != 200:
            return util.json_return(code, res)
        if _valid_chart(chart, res, df):
            charts.append(res)
    return util.json_return(code, charts)


def _valid_chart(chart, res, df):
    """
    To be implemented later, should validate the chart suggestion.
    """
    print(chart, res, df)
    return True


@bp.route('/ai-report-chart-suggest-from-existing', methods=['get'])
def specific_chart_suggest_with_existing_source():
    """
    The input is a chart and data.
    We suggest fields for a chart based on the provided data.
    """
    file_ok, ret = util.check_and_load_existing_file(request)
    try:
        chart = request.args.get('chart')
    except KeyError:
        return False, util.json_return(400, 'No chart type provided')
    if not file_ok:
        return ret
    df = pd.DataFrame(ret)

    if chart == 'line':
        chart = 'linechart'
    if chart == 'bar':
        chart = 'barchart'
    code, res = suggest_chart_fields_from_data(df, chart)
    # update `res` to be a substring starting with the first { and ending with the last }
    res = res[res.find('{'):res.rfind('}')+1]
    if code != 200:
        return util.json_return(code, res)
    return util.json_return(code, res)


@bp.route('/setup-chart-builder-assistant', methods=['get'])
def setup_chart_builder_assistant():
    """
    Setup the chart builder assistant.
    """
    code, res = create_chart_builder_assistant()
    return util.json_return(code, res)


@bp.route('/setup-iati-query-assistant', methods=['get'])
def setup_iati_query_assistant():
    """
    Setup the chart builder assistant.
    """
    code, res = create_iati_query_assistant()
    return util.json_return(code, res)
