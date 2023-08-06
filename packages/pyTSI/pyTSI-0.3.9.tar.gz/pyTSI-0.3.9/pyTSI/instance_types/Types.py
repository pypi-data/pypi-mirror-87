import logging
import requests
from .Type import Type
from ..environment import environment
from ..variables.Variable import variable_helper
from ..common.common_funcs import get_query_string, get_authorization_token


class Types:
    def __init__(self):
        """
        Types object

        This class implements the API for getting types from the TSI.
        Not to be confused with Type, which holds the actual types.
        """
        self.__types = None

    def __call__(self, *args, **kwargs):
        """
        Return the list of types in the TSI, optionally refreshing the list

        Parameters
        ----------
        args : ignored
        kwargs : keyword args
                 Supported vars are:

                    * force_refresh : bool
                                      Flag indicating whether the list should be
                                      forcefully re-read from the TSI.

        Returns
        -------
        List [ Type ] : The list of type
        """
        if kwargs.get('force_refresh', False):
            self.__refresh_types()

        return self._types

    def get_by_id(self, type_id, force_refresh=False):
        """
        Get a Type given its id

        Parameters
        ----------
        type_id : list [ str ]
                  List of up to three strings composing the time series ID

        force_refresh : bool
                        Flag indicating whether the type search should
                        unconditionally be performed online. If set to
                        `False` and a similar type has already been
                        searched for, a cached Type object will be
                        returned.

        Returns
        -------
        Type or None
        """
        # Check if we already know about the type, return it in that case
        if not force_refresh:
            if self.__types is not None and type_id in self.__types:
                return self.__types[type_id]

        # Look for types with the given ID
        response = self.__query_types(method='POST', batch=True,
                                      json={'get': {'typeIds': [type_id], 'names': None}})
        if len(response['get']) != 1 or 'error' in response['get'][0]:
            return None

        t = response['get'][0]['timeSeriesType']
        if self.__types is None:
            self.__types = dict()

        self.__types[t['id']] = Type(type_id=t['id'],
                                     name=t['name'],
                                     description=t.get('description'),
                                     vars=[variable_helper(k, v)
                                           for k, v in t['variables'].items()])

        return self.__types[t['id']]

    def get_by_name(self, type_name, force_refresh=False):
        """
        Get a Type given its name

        Parameters
        ----------
        type_name : str
                    Type name

        force_refresh : bool
                        Flag indicating whether the type search should
                        unconditionally be performed online. If set to
                        `False` and a similar type has already been
                        searched for, a cached Type object will be
                        returned.

        Returns
        -------
        Type or None
        """
        # Check if we already know about the type, return it in that case
        if not force_refresh:
            if self.__types is not None:
                candidates = [t for t in self.__types.values()
                              if t.name == type_name]
                if len(candidates) == 1:
                    return candidates[0]

        # Look for types with the given ID
        response = self.__query_types(method='POST', batch=True,
                                      json={'get': {'names': [type_name]}})
        if len(response['get']) != 1 or 'error' in response['get'][0]:
            return None

        t = response['get'][0]['timeSeriesType']
        if self.__types is None:
            self.__types = dict()

        self.__types[t['id']] = Type(type_id=t['id'],
                                     name=t['name'],
                                     description=t.get('description'),
                                     vars=[variable_helper(k, v)
                                           for k, v in t['variables'].items()])

        return self.__types[t['id']]

    @property
    def _types(self):
        if self.__types is None:
            self.__refresh_types()

        return self.__types.values()

    def __refresh_types(self):
        """
        Download the list of types from the TSI
        """
        response = self.__query_types()

        self.__types = dict()
        for t in response['types']:
            self.__types[t['id']] = Type(type_id=t['id'],
                                         name=t['name'],
                                         description=t.get('description'),
                                         vars=[variable_helper(k, v)
                                               for k, v in t['variables'].items()])

    @staticmethod
    def __query_types(method='GET', batch=False, json=None):
        url = f'https://{environment.ENVIRONMENT_ID}.env.timeseries.azure.com/timeseries/types'
        if batch:
            url = f'{url}/$batch'
        headers = {'x-ms-client-application-name': environment.APPLICATION_NAME,
                   'Authorization': get_authorization_token(),
                   'Content-Type': "application/json",
                   'cache-control': "no-cache"}

        try:
            response = requests.request(method, url, json=json, headers=headers,
                                        params=get_query_string(), timeout=10)
            response.raise_for_status()

        except requests.exceptions.ConnectTimeout:
            logging.error('pyTSI: The request to the TSI API timed out.')
            raise
        except requests.exceptions.HTTPError:
            logging.error('pyTSI: The request to the TSI API returned an unsuccessful status code.')
            raise

        return response.json()
