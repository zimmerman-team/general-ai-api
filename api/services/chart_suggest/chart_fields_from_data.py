import json

from api.services.openai.assistants import cb_assistant_prompt_with_storage

PREVIOUS_SUGGESTIONS_FILE = './api/services/chart_suggest/data/chart_fields_from_data_previous_suggestions.json'
DX_CHART_DEFINITIONS = './api/services/chart_suggest/data/dx_charts.json'


def suggest_chart_fields_from_data(df, chart):
    """
    Use openAI to suggest a chart type for the given columns and some example rows.

    param df: pandas dataframe containing the content of the uploaded CSV file
    """
    # Validate the selected chart type exists in our chart definitions
    chart_context = get_charts_semantic_context(chart)
    if not chart_context:
        return 400, "Chart type not supported."

    df_head = _sample_df(df)
    prompt = f"""Given your known chart descriptions, and given the following sample dataframe:\n{df_head}\n
        We want to generate a {chart}. {chart_context}
        Which columns would you assign to which inputs as mentioned above?
        If there is no fitting chart, please state so.
        If there is a size calculation required, recommend the most likely one,
        and if you cannot determine the most likely one use the sum.
        Please return your answer as a JSON object.
        If size is required, for size, use the column as the key and the size as the value.
        If we are generating one of the following: linechart, areachart, bubblechart, heatmap, areatimeaxis, areastack, or scatterchart, please use the keys 'x' and 'y' for the x and y axis respectively, and for the lines use lowercase lines.
        If we are generating a linechart, areatimeaxis, or areastack, for the y axis, instead of just the column name, return a key value pair where the key is the column name, and the value the aggregation function (default to count).
        For keys in your JSON object, make sure they are always lowercase.
        Please include a short title for the chart under the key 'title'. And the value {chart} under the key 'chartType'.
        If you have an explanation for your answer, please include it in the JSON object under the key 'explanation'."""  # NOQA: E501

    return cb_assistant_prompt_with_storage(df_head, PREVIOUS_SUGGESTIONS_FILE, prompt, chart)


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


def _sample_df(df):
    """
    Sample size should be more than 4 rows, but not too large as to not overwhelm the LLM with too much information.

    :param df: pandas dataframe
    """
    n_rows_df = df.shape[0]
    n_head = n_rows_df
    if n_rows_df > 50:
        n_head = 50
    head = df.head(n_head).to_string()
    while len(head) > 100000:  # We can send up to 128k tokens, this limits the dataset size.
        n_head = n_head // 2
        if n_head == 0:
            n_head = 1
            break
        head = df.head(n_head).to_string()
    return head
