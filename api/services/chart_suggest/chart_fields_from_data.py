import json

from api.services.openai.prompt import prompt_with_storage

PREVIOUS_SUGGESTIONS_FILE = './api/services/chart_suggest/data/chart_fields_from_data_previous_suggestions.json'
DX_CHART_DEFINITIONS = './api/services/chart_suggest/data/dx_charts.json'


def suggest_chart_fields_from_data(df, chart):
    """
    Use openAI to suggest a chart type for the given columns and some example rows.

    param df: pandas dataframe containing the content of the uploaded CSV file
    """
    chart_context = get_charts_semantic_context(chart)
    if not chart_context:
        return 400, "Chart type not supported."

    df_head = df.head().to_string()
    prompt = f"""Given the following sample dataframe:\n{df_head}\n
        We want to generate a {chart}. {chart_context}
        Which columns would you assign to which inputs as mentioned above?
        If there is no fitting chart, please state so.
        If there is a size calculation required, recommend the most likely one,
        and if you cannot determine the most likely one use the sum.
        Please return your answer as a JSON object. For size, use the column as the key and the size as the value.
        If we are generating a linechart, please use the keys 'x' and 'y' for the x and y axis respectively, and for the lines use lowercase lines.
        Please include a short title for the chart under the key 'title'. And the value {chart} under the key 'chartType'.
        If you have an explanation for your answer, please include it in the JSON object under the key 'explanation'."""

    return prompt_with_storage(df_head, PREVIOUS_SUGGESTIONS_FILE, prompt, chart)
    # Check if we've created suggestions for this exact dataframe before.


def get_charts_semantic_context(chart):
    """
    Get the semantic context for a given chart type.

    :param chart: the chart type
    :return: the semantic context
    """
    with open(DX_CHART_DEFINITIONS, 'r') as f:
        chart_definitions = json.load(f)
        if chart not in chart_definitions:
            return None
        return chart_definitions[chart]['semantic']
