## Character API Autotests

![Test Automation](https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExdTlsbWh0Z3Z4OTdramJ1dzdteTJvcXJvM2g0a3Q5ajZvY3p5bm1jZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QXwtfadqo7wbfmT46H/giphy.gif)

This project contains tests for the [Ivi Character API](https://rest.test.ivi.ru/v2), written using
the pytest library.

### Setup Requirements

Before you start, ensure you have Python and the necessary dependencies installed. To install the
dependencies, execute:

    pip install -r requirements.txt

#### Setup the env urls into config.py

      API_URLS = {
          'dev': 'http://dev.rest.test.ivi.ru/v2',
          'prod': 'http://rest.test.ivi.ru/v2'
      }

#### Setup the .env file

      ENV=prod
      API_USERNAME=
      API_PASSWORD=

## Running Tests

Running Tests from the Terminal
To run tests without environment variables, use the following command:

    pytest tests/integration/test_character_api.py --alluredir=allure_results

Running Tests with Environment Variables

To run tests with the environment variable (by default ENV=prod), execute:

    ENV=prod pytest tests/integration/test_character_api.py --alluredir=allure_results

Running Tests in Multithreaded Mode using pytest-xdist:

To run tests in multithreaded mode with the environment variable, use:

    ENV=prod pytest tests/integration/test_character_api.py --alluredir=allure_results -n auto

## Running Tests via Docker

![Docker](https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNnJ5Z2lqM2VtZmZyb2YyYTFudndsbnowbnhza3FleG8zdnhveWJuMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bi34AxJHYSsJljAqGZ/giphy.gif)

If you prefer to run tests in a Docker container, execute the following commands:

Build the Docker Image:

    docker build -t character-api-tests .

Run the Container with the Environment Variable ENV=prod:

    docker run --rm -e ENV=prod character-api-tests

### Generating Allure Reports

After running the tests with the --alluredir=allure_results parameter, you can generate an Allure report by
executing the following command:

    allure serve allure_results
