# Zimmerman General AI API
This is a runnable service that provides access to general AI services developed by Zimmerman.

## Development
Check out [Docker](#docker) for a quickstart guide.

The application was developed on python 3.11.2, with [flask](https://flask.palletsprojects.com/en/2.2.x/) as its base<br />
Install the requirements with `pip install -r requirements.txt`.<br />
Make sure to run `pre-commit install --hook-type commit-msg` to enable the commit hooks.<br />
[api/\_\_init\_\_.py](api/__init__.py) defines the entrypoint for the application, which is started from [manage.py](manage.py)<br />
Running the API can be done locally with `flask run`. This starts the flask app 'api' due to the [.flaskenv settings](.flaskenv).<br />

### Environment
Use the .env.example file. Notable fields:
- `AIAPI_OPENAI_API_KEY`: found in [openAI settings](https://platform.openai.com/account/api-keys). Used for semantic searching.
- `AIAPI_API_KEY`: required, can generate any key string, required to access the API to prevent abuse.

### API Directory
- The models are the data descriptor of our application, in many cases related to the database model. How each model is defined will heavily depend on the library you use to connect to your database.
- The routes are the URIs to our application, where we define our resources and actions.
- The schemas are the definitions for inputs and outputs of our API, what parameters are allowed, what information we will output. They correlate to our resources, but they are not necessarily the same as our models.
- The services are modules that define application logic or interact with other services or the db layer. Routes should be as simple as possible and delegate all logic to the services.

### Packages
- openai
- python-dotenv
- flake8
- isort
- pre-commit
- flake8-isort
- flask
- gunicorn
- pandas
- tiktoken
- regex
- seaborn

### Code quality
*flake8* is used to maintain code quality in pep8 style<br />
*isort* is used to maintain the imports<br />
*pre-commit* is used to enforce commit styles in the form<br />
```
feat: A new feature
fix: A bug fix
docs: Documentation only changes
style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
refactor: A code change that neither fixes a bug nor adds a feature
perf: A code change that improves performance
test: Adding missing or correcting existing tests
chore: Changes to the build process or auxiliary tools and libraries such as documentation generation
```

## API Routes
[API Routes documentation](api/routes/README.md)

## Available services
- Chart suggestion: providing a CSV file and either receiving recommendations of chart types with fields to use, or providing a CSV file and a chart type, and receiving recommendations for the most likely useful chart.

## Docker
[Install docker](https://docs.docker.com/get-docker/) (make sure docker compose is installed).

Once the .env file is set up, use the [docker-compose](docker-compose.yml) file to run the API.
```
docker compose up
```

Will start (and build if this is the first time running) the API, alongside NGINX to provide access to the API.<br />
Re-build with `docker compose up --build`<br />
Shut down with `docker compose down`

Note: We've changed from `alpine` to `slim` to reduce buildtime by 50x.