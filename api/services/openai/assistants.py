import hashlib
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_CLIENT = OpenAI(api_key=os.environ.get("AIAPI_OPENAI_API_KEY"))
ASSISTANT_ID = os.environ.get("AIAPI_OPENAI_CB_ASSISTANT_ID")
IATI_QUERY_ASSISTANT_ID = os.environ.get("AIAPI_OPENAI_IQ_ASSISTANT_ID")
AIAPI_OPENAI_MODEL = "gpt-4o-mini"
DX_CHART_DEFINITIONS = "./api/services/chart_suggest/data/dx_charts.json"
IATI_QUERY_INSTRUCTION = """
You are a helpful Solr 9.10 query building assistant.

We are querying IATI data, from the International Aid Transparency Initiative. Make sure to use that as context for your search. 

This is the base URL that we use: "https://datastore.iati.cloud/api/v2/activity/?q=*:*"
We need you to construct the q=*:* to whatever matches the content of the query.

These are the available fields that can be searched for, their names should help you identify useful fields for the query, based on the search input. Please make sure, for every part of the query, that you consider all possible related fields.
AVAILABLE_FIELDS = [
 "iati_identifier",
 "reporting_org_ref",
 "reporting_org_narrative",
 "title_narrative",
 "description_narrative",
 "participating_org_ref",
 "participating_org_type",
 "participating_org_role",
 "participating_org_narrative",
 "other_identifier_ref",
 "activity_status_code",
 "activity_date_start_planned_f",
 "activity_date_start_actual_f",
 "activity_date_end_planned_f",
 "activity_date_end_actual_f",
 "contact_info_email",
 "activity_scope_code",
 "recipient_country_code",
 "recipient_country_name",
 "recipient_region_code",
 "recipient_region_name",
 "location_name_narrative",
 "location_description_narrative",
 "location_administrative_code",
 "sector_code",
 "sector_narrative",
 "tag_code",
 "tag_vocabulary",
 "tag_narrative",
 "policy_marker_code",
 "policy_marker_significance",
 "collaboration_type_code",
 "default_flow_type_code",
 "default_finance_type_code",
 "default_aid_type_code",
 "default_tied_status_code",
 "planned_disbursement_provider_org_ref",
 "planned_disbursement_provider_org_narrative",
 "planned_disbursement_receiver_org_ref",
 "planned_disbursement_receiver_org_narrative",
 "capital_spend_percentage",
 "transaction_provider_org_ref",
 "transaction_provider_org_narrative",
 "transaction_receiver_org_ref",
 "transaction_receiver_org_narrative",
 "document_link_title_narrative",
 "document_link_description_narrative",
 "document_link_category_code",
 "document_link_language_code",
 "document_link_document_date_iso_date",
 "related_activity_ref",
 "related_activity_type",
 "result_description_narrative",
]

I want to you to change the query url to something that matches this search input. Ensure that the resulting query url is a valid SOLR query URL. 

Make sure to apply these rules when building the query:
Date fields are in the DatePointField format, so dates should use this format: "YYYY-MM-DDThh:mm:ssZ". For countries, consider the full names, and ISO2 and ISO3 codes, and don't forget to consider the location fields. 
For organisations, it is helpful to look in the related "_ref" fields with ISO2 codes, postfixed with an asterisk for wildcard searching. If the query mentions organisations, assume we want to look for any type of related organisation, except when it is explicitly mentioned that they should only be participating or reporting organisations.

In your response, provide a JSON object which has structure:
{
  url: the updated URL,
  explanation: the reason why you generated this url.
}
"""  # NOQA: 501


def create_chart_builder_assistant():
    try:
        # Create the assistant for file search
        assistant = OPENAI_CLIENT.beta.assistants.create(
            name="ChartBuilderAssistant",
            instructions="You are a chart type expert. Use your knowledge base to answer questions about charts, their mapping and their semantic context. In your answers about charts, only use the exact chart types, mappings and semantic descriptions of those charts, as found in the file DXChartDefinitions",  # NOQA: E501
            model=AIAPI_OPENAI_MODEL,
            tools=[{"type": "file_search"}],
        )

        # Create the vector store for the DX Charts definitions
        vector_store = OPENAI_CLIENT.beta.vector_stores.create(name="DXChartDefinitions")
        file_paths = [DX_CHART_DEFINITIONS]
        file_streams = [open(path, "rb") for path in file_paths]
        file_batch = OPENAI_CLIENT.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams
        )

        # Verify file upload status
        print(file_batch.status)
        print(file_batch.file_counts)
        if file_batch.status == "failed":
            print(file_batch.error)

        # Update the assistant to enable file search in the DX Chart Definitions
        assistant = OPENAI_CLIENT.beta.assistants.update(
            assistant_id=assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        )
    except Exception as e:
        err = "Error in create_chart_builder_assistant: " + str(e)
        print(err)
        return 500, err
    return 200, "Success"


# print(create_chart_builder_assistant())  # Uncomment to quickly execute the function with `python ./api/services/openai/assistants.py`  # NOQA: E501


def cb_assistant_prompt_with_storage(df_head, storage_file, prompt, hash_modifier=""):
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

    if len(prompt) > 128000:
        return 400, "The prompt is too long. The maximum length is 128000 characters."

    try:
        # Generate Suggestion with GPT-4o-mini through the selected assistant
        print("prompt_with_storage -- No previous suggestion found. Creating new suggestion.")
        assistant = OPENAI_CLIENT.beta.assistants.retrieve(ASSISTANT_ID)
        # Create a thread and attach the file to the message
        thread = OPENAI_CLIENT.beta.threads.create(
            messages=[{"role": "user", "content": prompt}]
        )
        run = OPENAI_CLIENT.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id
        )
        messages = list(OPENAI_CLIENT.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
        res = messages[0].content[0].text.value
        res = _parse_res(res)
        print("ASSISTANT:: prompt res:", res)
        # Add an object with the hash as key and the result as value to, and add it to the previous suggestions file.
        with open(storage_file, 'r') as f:
            previous_suggestions = json.load(f)
            previous_suggestions[md5_hash] = res
        with open(storage_file, 'w') as f:
            json.dump(previous_suggestions, f)
        return 200, res
    except Exception as e:
        res = "Error in assistant prompt_with_storage: " + str(e)
        print(res)
        return 500, res


def _parse_res(res):
    # if res starts with ```json\n, remove it
    if res.startswith("```json\n"):
        res = res[7:]
    if res.endswith("\n```"):
        res = res[:-4]
    return res


def create_iati_query_assistant():
    try:
        OPENAI_CLIENT.beta.assistants.create(
            name="IATISolrQueryBuilder",
            instructions=IATI_QUERY_INSTRUCTION,
            model=AIAPI_OPENAI_MODEL,
        )
    except Exception as e:
        err = "Error in create_iati_query_assistant: " + str(e)
        return 500, err
    return 200, "Success"


def iq_assistant_prompt(user_input):
    status, url = _convert_user_input_to_query(user_input)
    return status, url


def _convert_user_input_to_query(user_input):
    # connect to openAI assistant
    try:
        OPENAI_CLIENT = OpenAI(api_key=os.environ.get("AIAPI_OPENAI_API_KEY"))
        assistant = OPENAI_CLIENT.beta.assistants.retrieve(IATI_QUERY_ASSISTANT_ID)
        # Create a thread and attach the file to the message
        thread = OPENAI_CLIENT.beta.threads.create(
            messages=[{"role": "user", "content": user_input}]
        )
        run = OPENAI_CLIENT.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id
        )
        messages = list(OPENAI_CLIENT.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
        res = messages[0].content[0].text.value
    except Exception:
        return "Unable to connect to the IATI Query Assistant", None
    try:
        # read res as json
        res = json.loads(res)
        url = res.get("url")
    except Exception:
        return "Error parsing assistant response", None
    return "OK", url
