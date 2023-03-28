from os import environ


API_KEY = environ.get('API_KEY', '')
OPENAI_API_KEY = environ.get('OPENAI_API_KEY', '')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

# Additional flask settings
FLASK_DEBUG = environ.get('FLASK_DEBUG', False)
