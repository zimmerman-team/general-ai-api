import os
import hashlib
import json

import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")
PREVIOUS_SUGGESTIONS_FILE = './api/services/chart_suggest/previous_suggestions.json'


def suggest_chart_for_csv_file(df):
    """
    Use openAI to suggest a chart type for the given columns and some example rows.

    param df: pandas dataframe containing the content of the uploaded CSV file
    """
    df_head = df.head().to_string()
    # Check if we've created suggestions for this exact dataframe before.
    md5_hash = hashlib.md5(df_head.encode()).hexdigest()
    with open(PREVIOUS_SUGGESTIONS_FILE, 'r') as f:
        previous_suggestions = json.load(f)
        if md5_hash in previous_suggestions:
            print("Returning existing previous suggestion.")
            return previous_suggestions[md5_hash]

    # Generate suggestions using gpt3.5 turbo.
    print("No previous suggestion found. Creating new suggestion.")
    prompt = f"""Given the following sample dataframe:\n{df_head}\n
        What are 5 chart types you would use to visualize this data?
        And which columns would you use in which dimension of the charts?"""
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    res = completion.choices[0].message.content
    # Add an object with the hash as key and the result as value to, and add it to ./previous_suggestions.json
    with open(PREVIOUS_SUGGESTIONS_FILE, 'r') as f:
        previous_suggestions = json.load(f)
        previous_suggestions[md5_hash] = res
    with open(PREVIOUS_SUGGESTIONS_FILE, 'w') as f:
        json.dump(previous_suggestions, f)
    return res
