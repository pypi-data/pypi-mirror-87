import logging
import requests
from ..environment import environment
from ..instance_types.Types import Types
from ..common.common_funcs import get_query_string, get_authorization_token
from .TimeSeriesInstance import TimeSeriesInstance


class TimeSeries:
    def __init__(self, types):
        """
        Time Series object

        This class implements the API for getting time series.
        Not to be confused with TimeSeriesInstance, which holds the actual
        instances.

        Parameters
        ----------
        types : Types
                The list of types available for the current TSI series
        """
        self._types = types
        self.__time_series = None

    def get_by_id(self, time_series_id, force_refresh=False):
        """
        Get a TimeSeriesInstance by its ID

        Parameters
        ----------
        time_series_id : list [ str ]
                         A list of IDs providing a unique key for the series.
        force_refresh : bool
                        Flag indicating whether the server should be queried or
                        cached data should be used

        Returns
        -------
        TimeSeriesInstance or None
        """
        # We must store the time series type ID as a tuple, since lists are not hashable :(
        time_series_id = tuple(time_series_id)
        if not force_refresh:
            if self.__time_series is not None and time_series_id in self.__time_series:
                return self.__time_series[time_series_id]

        # Look for the series definition in the TSI
        json = {'get': {'timeSeriesIds': [time_series_id]}}
        response = self.__query_instances(method='POST', batch=True, json=json)
        if len(response['get']) != 1 or 'error' in response['get'][0]:
            return None
        ts = response['get'][0]['instance']
        if self.__time_series is None:
            self.__time_series = dict()

        # Retrieve the series type
        series_type = self._types.get_by_id(ts['typeId'])
        if series_type is None:
            # Should probably not happen, really
            raise RuntimeError('The type id for the given series is not valid')

        time_series_id = tuple(ts['timeSeriesId'])
        self.__time_series[time_series_id] = TimeSeriesInstance(series_type=series_type,
                                                                series_id=ts['timeSeriesId'],
                                                                name=ts.get('name'),
                                                                description=ts.get('description'),
                                                                instance_fields=ts.get('instanceFields'))
        return self.__time_series[time_series_id]

    def get_by_name(self, time_series_name, force_refresh=False):
        """
        Get a TimeSeriesInstance given its name

        Parameters
        ----------
        time_series_name : str
                           The time series name
        force_refresh : bool
                        Flag indicating whether the server should be queried or
                        cached data should be used

        Returns
        -------
        TimeSeriesInstance or None
        """
        if not force_refresh:
            if self.__time_series is not None:
                candidates = [ts for ts in self.__time_series.values()
                              if ts.name == time_series_name]
                if len(candidates) == 1:
                    return candidates[0]

        # Look for the series definition in the TSI
        json = {'get': {'names': [time_series_name]}}
        response = self.__query_instances(method='POST', batch=True, json=json)
        if len(response['get']) != 1 or 'error' in response['get'][0]:
            return None
        ts = response['get'][0]['instance']
        if self.__time_series is None:
            self.__time_series = dict()

        # Retrieve the series type
        series_type = self._types.get_by_id(ts['typeId'])
        if series_type is None:
            # Should probably not happen, really
            raise RuntimeError('The type id for the given series is not valid')

        time_series_id = tuple(ts['timeSeriesId'])
        self.__time_series[time_series_id] = TimeSeriesInstance(series_type=series_type,
                                                                series_id=ts['timeSeriesId'],
                                                                name=ts.get('name'),
                                                                description=ts.get('description'),
                                                                instance_fields=ts.get('instanceFields'))
        return self.__time_series[time_series_id]

    def __call__(self, *args, **kwargs):
        """
        Return the list of instances in the TSI, optionally refreshing the list

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
        List [ TimeSeriesIntance ] : The list of time series instances
        """
        if kwargs.get('force_refresh', False):
            self.__refresh_series()

        return self._time_series

    @property
    def _time_series(self):
        if self.__time_series is None:
            self.__refresh_series()

        return self.__time_series.values()

    def __refresh_series(self):
        """
        Download the list of Time Series Instances from the TSI
        """
        json_response = self.__query_instances()

        self.__time_series = {
            tuple(ts['timeSeriesId']): TimeSeriesInstance(series_type=[t for t in self._types(force_refresh=True)
                                                                       if ts['typeId'] == t.type_id][0],
                                                          series_id=ts['timeSeriesId'],
                                                          name=ts.get('name'),
                                                          description=ts.get('description'),
                                                          instance_fields=ts.get('instanceFields'))
            for ts in json_response['instances']}

    @staticmethod
    def __query_instances(method='GET', batch=False, json=None):
        url = f'https://{environment.ENVIRONMENT_ID}.env.timeseries.azure.com/' \
              f'timeseries/instances/'
        if batch:
            url = f'{url}/$batch'
        authorization_token = get_authorization_token()
        querystring = get_query_string()
        headers = {
            'x-ms-client-application-name': environment.APPLICATION_NAME,
            'Authorization': authorization_token,
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        try:
            response = requests.request(method, url, json=json, headers=headers,
                                        params=querystring, timeout=10)
            response.raise_for_status()

        except requests.exceptions.ConnectTimeout:
            logging.error('pyTSI: The request to the TSI API timed out.')
            raise
        except requests.exceptions.HTTPError:
            logging.error('pyTSI: The request to the TSI API returned an unsuccessful status code.')
            raise

        json_response = response.json()

        while 'continuationToken' in json_response.keys():
            headers = {
                'x-ms-client-application-name': environment.APPLICATION_NAME,
                'Authorization': authorization_token,
                'x-ms-continuation': json_response['continuationToken'],
                'Content-Type': "application/json",
                'cache-control': "no-cache"
            }
            response = requests.request(method, url, json=json,
                                        headers=headers, params=querystring)
            json_response = {**json_response, **response.json()}

        return json_response
