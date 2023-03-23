# Zimmerman General AI API
This is a runnable service that provides access to general AI services developed by Zimmerman.

## Development
The application was developed on python 3.11.2, with [flask](https://flask.palletsprojects.com/en/2.2.x/) as its base<br />
Install the requirements with `pip install -r requirements.txt`.<br />
Make sure to run `pre-commit install --hook-type commit-msg` to enable the commit hooks.<br />
[api/\_\_init\_\_.py](api/__init__.py) defines the entrypoint for the application, which is started from [manage.py](manage.py)<br />
Running the API can be done locally with `flask run`. This starts the flask app 'api' due to the [.flaskenv settings](.flaskenv).<br />

### API Directory
- The models are the data descriptor of our application, in many cases related to the database model. How each model is defined will heavily depend on the library you use to connect to your database.
- The routes are the URIs to our application, where we define our resources and actions.
- The schemas are the definitions for inputs and outputs of our API, what parameters are allowed, what information we will output. They correlate to our resources, but they are not necessarily the same as our models.
- The services are modules that define application logic or interact with other services or the db layer. Routes should be as simple as possible and delegate all logic to the services.

### Code quality
*flake8* is used to maintain code quality in pep8 style

*isort* is used to maintain the imports

*pre-commit* is used to enforce commit styles in the form
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
We are currently at the base implementation, so no services yet included.