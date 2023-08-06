import requests
import logging
import json
from . import environment
from ..exceptions import TSIEnvironmentError
from ..common.common_funcs import get_query_string, get_authorization_token


class EnvironmentApi:
    def __init__(self):
        pass

    def get_environment_id(self):
        """Gets the id of the environment specified in the TSIClient class constructor.

        Returns:
            str: The environment id.

        Raises:
            TSIEnvironmentError: Raised if the TSI environment does not exist.
        """

        authorization_token = get_authorization_token()
        url = "https://api.timeseries.azure.com/environments"

        querystring = get_query_string()

        payload = ""
        headers = {
            "x-ms-client-application-name": environment.APPLICATION_NAME,
            "Authorization": authorization_token,
            "Content-Type": "application/json",
            "cache-control": "no-cache",
        }

        try:
            response = requests.request(
                "GET",
                url,
                data=payload,
                headers=headers,
                params=querystring,
                timeout=10,
            )
            response.raise_for_status()
        except requests.exceptions.ConnectTimeout:
            logging.error("pyTSI: The request to the TSI api timed out.")
            raise
        except requests.exceptions.HTTPError:
            logging.error(
                "pyTSI: The request to the TSI api returned an unsuccessfull status code."
            )
            raise

        environments = json.loads(response.text)['environments']
        environment_id = None
        for env in environments:
            if env["displayName"] == environment.ENVIRONMENT_NAME:
                environment_id = env['environmentId']
                break
        if environment_id is None:
            raise TSIEnvironmentError(
                'pyTSI: TSI environment not found. Check the spelling or create an environment in Azure TSI.'
            )

        return environment_id

    def get_environment_availability(self):
        """Returns the time range and distribution of event count over the event timestamp.
        Can be used to provide landing experience of navigating to the environment.

        Returns:
            dict: The environment availability. Contains interval size, distribution and range.
        """

        authorizationToken = get_authorization_token()
        url = f'https://{environment.ENVIRONMENT_ID}.env.timeseries.azure.com/availability'
        querystring = get_query_string()
        payload = ""
        headers = {
            'x-ms-client-application-name': environment.APPLICATION_NAME,
            'Authorization': authorizationToken,
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        try:
            response = requests.request(
                "GET",
                url,
                data=payload,
                headers=headers,
                params=querystring,
                timeout=10
            )
            response.raise_for_status()
        except requests.exceptions.ConnectTimeout:
            logging.error("pyTSI: The request to the TSI api timed out.")
            raise
        except requests.exceptions.HTTPError:
            logging.error("pyTSI: The request to the TSI api returned an unsuccessfull status code.")
            raise

        return json.loads(response.text)
