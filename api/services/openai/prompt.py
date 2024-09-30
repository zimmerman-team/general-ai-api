import hashlib
import json
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("AIAPI_OPENAI_API_KEY"))

OPENAI_MODEL = "gpt-4o-mini"
OPENAI_MODEL_COMPLETION = "gpt-3.5-turbo-instruct"


def prompt_with_storage(df_head, storage_file, prompt, hash_modifier="", temperature=1):
    """
    Submit the provided prompt to openAI and return the result.
    If the result has already been generated before, return the previous result instead.

    This function submits the prompt to OPENAI_MODEL, recommended use is gpt-3.5-turbo.

    :param df_head: The head of the dataframe used for hashing.
    :param storage_file: The file to store the previous suggestions in.
    :param prompt: The prompt to submit to openAI.
    :param hash_modifier: A string to add to the hash to make it unique.
    """
    # Check if we've created suggestions for this exact dataframe before.
    md5_hash = hash_modifier+hashlib.md5(df_head.encode()).hexdigest()

    with open(storage_file, 'r') as f:
        previous_suggestions = json.load(f)
        if md5_hash in previous_suggestions:
            print("prompt_with_storage -- Returning existing previous suggestion.")
            return 200, previous_suggestions[md5_hash]

    try:
        # # Generate suggestions using gpt3.5 turbo.
        print("prompt_with_storage -- No previous suggestion found. Creating new suggestion.")
        completion = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        res = completion.choices[0].message.content
        # Add an object with the hash as key and the result as value to, and add it to the previous suggestions file.
        with open(storage_file, 'r') as f:
            previous_suggestions = json.load(f)
            previous_suggestions[md5_hash] = res
        with open(storage_file, 'w') as f:
            json.dump(previous_suggestions, f)
        return 200, res
    except Exception as e:
        res = "Error in prompt_with_storage: " + str(e)
        print(res)
        return 500, res


def prompt_with_storage_completion(df_head, storage_file, prompt, hash_modifier="", temperature=1):
    """
    Submit the provided prompt to openAI and return the result.
    If the result has already been generated before, return the previous result instead.

    This function submits the prompt to OPENAI_MODEL, recommended use is gpt-3.5-turbo.

    :param df_head: The head of the dataframe used for hashing.
    :param storage_file: The file to store the previous suggestions in.
    :param prompt: The prompt to submit to openAI.
    :param hash_modifier: A string to add to the hash to make it unique.
    """
    # Check if we've created suggestions for this exact dataframe before.
    md5_hash = hash_modifier+hashlib.md5(df_head.encode()).hexdigest()

    with open(storage_file, 'r') as f:
        previous_suggestions = json.load(f)
        if md5_hash in previous_suggestions:
            print("prompt_with_storage -- Returning existing previous suggestion.")
            return 200, previous_suggestions[md5_hash]

    try:
        # # Generate suggestions using gpt3.5 turbo.
        print("prompt_with_storage -- No previous suggestion found. Creating new suggestion.")
        completion = client.completions.create(
            model=OPENAI_MODEL_COMPLETION,
            prompt=prompt,
            temperature=temperature
        )
        res = completion.choices[0].text
        # strip any newLines from the result
        res = res.replace("\n", "")
        # if there are spaces in the result, split it and concatenate it with a +
        if " " in res:
            res = "+".join(res.split(" "))
        # Add an object with the hash as key and the result as value to, and add it to the previous suggestions file.
        with open(storage_file, 'r') as f:
            previous_suggestions = json.load(f)
            previous_suggestions[md5_hash] = res
        with open(storage_file, 'w') as f:
            json.dump(previous_suggestions, f)
        return 200, res
    except Exception as e:
        res = "Error in prompt_with_storage: " + str(e)
        print(res)
        return 500, res
