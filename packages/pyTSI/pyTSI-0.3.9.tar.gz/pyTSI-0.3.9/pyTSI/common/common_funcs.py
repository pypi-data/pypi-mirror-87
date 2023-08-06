import logging
import requests
from ..environment import environment


def get_query_string(use_warm_store=None):
    """Creates the querystring for an api request.

    Can be used in all api requests in pyTSI.

    Args:
        use_warm_store (bool): A boolean to indicate the storeType. Defaults to None,
            in which case no storeType param is included in the querystring.

    Returns:
        dict: The querystring with the api-version and optionally the storeType.
    """

    if use_warm_store is None:
        return {'api-version': environment.API_VERSION}

    else:
        return {
            'api-version': environment.API_VERSION,
            'storeType': 'WarmStore' if use_warm_store else 'ColdStore'
        }


def get_authorization_token():
    """Gets an authorization token from the Azure TSI api which is used to authenticate api calls.

    Returns:
        str: The authorization token.
    """

    url = 'https://login.microsoftonline.com/{0!s}/oauth2/token'.format(environment.TENANT_ID)

    payload = {
        "grant_type": "client_credentials",
        "client_id": environment.CLIENT_ID,
        "client_secret": environment.CLIENT_SECRET,
        "resource": "https%3A%2F%2Fapi.timeseries.azure.com%2F&undefined=",
    }

    payload = "grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}&resource={resource}".format(
        **payload
    )

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "cache-control": "no-cache",
    }

    try:
        response = requests.request(
            "POST", url, data=payload, headers=headers, timeout=10
        )
        response.raise_for_status()
    except requests.exceptions.ConnectTimeout:
        logging.error("pyTSI: The request to the TSI API timed out.")
        raise
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        if status_code == 401:
            logging.error('pyTSI: Authentication with the TSI API was '
                          'unsuccessful. Check your client secret.')
        else:
            logging.error('pyTSI: The request to the TSI api returned an '
                          'unsuccessfull status code. Check the stack trace')
        raise e

    response = response.json()
    return f'{response["token_type"]} {response["access_token"]}'