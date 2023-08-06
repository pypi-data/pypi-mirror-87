from ..common.common_funcs import get_query_string, get_authorization_token
from ..environment import environment
import requests
import json
import logging


class HierarchiesApi:
    def __init__(self):
        pass

    def get_hierarchies(self):
        """Gets all hierarchies from the specified TSI environment.

        Returns:
            dict: The hierarchies in form of the response from the TSI api call.
            Contains hierarchy id, names and source fields per hierarchy.

        Example:
            >>> from pyTSI import TSIClient as tsi
            >>> client = tsi.TSIClient()
            >>> hierarchies = client.hierarchies.get_hierarchies()
        """

        authorizationToken = get_authorization_token()

        url = f'https://{environment.ENVIRONMENT_ID}.env.timeseries.azure.com/timeseries/hierarchies'
        querystring = get_query_string()
        payload = ""
        headers = {
            'x-ms-client-application-name': environment.APPLICATION_NAME,
            'Authorization': authorizationToken,
            'Content-Type': "application/json",
            'cache-control': "no-cache",
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
            if response.text:
                jsonResponse = json.loads(response.text)

            result = jsonResponse

            while len(jsonResponse['hierarchies']) > 999 and 'continuationToken' in list(jsonResponse.keys()):
                headers = {
                    'x-ms-client-application-name': environment.APPLICATION_NAME,
                    'Authorization': authorizationToken,
                    'x-ms-continuation': jsonResponse['continuationToken'],
                    'Content-Type': "application/json",
                    'cache-control': "no-cache"
                }
                response = requests.request(
                    "GET",
                    url,
                    data=payload,
                    headers=headers,
                    params=querystring
                )
                if response.text:
                    jsonResponse = json.loads(response.text)

                result['hierarchies'].extend(jsonResponse['hierarchies'])

        except requests.exceptions.ConnectTimeout:
            logging.error('pyTSI: The request to the TSI API timed out.')
            raise
        except requests.exceptions.HTTPError:
            logging.error('pyTSI: The request to the TSI API returned an unsuccessfull status code.')
            raise

        return result
