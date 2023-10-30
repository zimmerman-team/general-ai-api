from os import environ


AIAPI_API_KEY = environ.get('AIAPI_API_KEY', '')
AIAPI_OPENAI_API_KEY = environ.get('AIAPI_OPENAI_API_KEY', '')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
# For DX Datasets
AIAPI_PARSED_DATA_FILES = environ.get('AIAPI_PARSED_DATA_FILES', './')

# Additional flask settings
FLASK_DEBUG = environ.get('FLASK_DEBUG', False)
