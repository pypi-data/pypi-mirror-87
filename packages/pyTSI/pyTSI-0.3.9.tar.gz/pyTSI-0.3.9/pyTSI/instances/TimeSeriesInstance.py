import json
import logging
import requests
import datetime
import pandas as pd
from ..environment import environment
from ..instance_types.Type import Type
from ..variables.Variable import NumericVariable
from ..common.common_funcs import get_query_string, get_authorization_token


class TimeSeriesInstance:
    def __init__(self, series_type, series_id, name, description, instance_fields):
        """
        Time Series Instance object

        Parameters
        ----------
        series_type : Type
                      The Type of the series instance to be created.
        series_id : List [ str ]
                    The ID for the time series. Must be a list of up to 3 strings.
        name : str
                      Name of the time series instance.
        description : str
                             Description of the time series instance.
        instance_fields : dict
                                 Dictionary of instance fields.
        """
        self.series_type = series_type
        self.series_id = series_id
        self.name = name
        self.description = description
        self.instance_fields = instance_fields

    def get_events(self, start, end, variables=None,
                   filter_tsx=None, use_warm_store=False,
                   drop_nans=False):
        """
        Get the raw events for the given Time Series Variables

        Please note that the API is limited to 250000 events.

        More information:
            https://docs.microsoft.com/en-us/rest/api/time-series-insights/dataaccessgen2/query/execute#getevents

        Parameters
        ----------
        start : datetime.datetime
                Initial instant
        end : datetime.datetime
              Final instant
        variables : list [ NumericVariable ] or None, optional
                    Variables whose data should be retrieved for the given
                    time series instances. The variables must be defined
                    in the TSI.

                    If not provided, all the variables for the type associated
                    with this time series will be fetched.
        filter_tsx : str, optional
                     Top-level filter string, can be None.
        use_warm_store : bool
                         Flag indicating whether the warm store shouldbe used.
        drop_nans : bool
                    Flag indicating whether rows of data that are only filled
                    with NaNs should be dropped from the returned DataFrame or
                    whether data should be returned exactly as provided by the
                    TSI.

        Returns
        -------
        pd.DataFrame
            Events for the given timespan, merged into a single DataFrame.
        """
        # Input data sanity check
        if variables is None:
            # Dirty hack to try to make sure that the projected properties call below will work
            variables = [v for v in self.series_type.vars
                         if isinstance(v, NumericVariable) and
                         v.var_value_tsx.split('.')[-1] in ('Double', 'Long')]
        if start >= end:
            raise ValueError('End time must be greater than start time')
        if start.tzinfo is not None:
            start = start.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        if end.tzinfo is not None:
            end = end.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        for ts_var in variables:
            if not isinstance(ts_var, NumericVariable):
                raise ValueError(f'Cannot operate on non-numeric var {ts_var} for {self}')

        # The payload we'll use for requesting data from the TSI
        # TODO: Setting the type as I do below will crash
        payload = {
            'getEvents': {
                "timeSeriesId": self.series_id,
                "searchSpan": {"from": f'{start.isoformat()}Z',
                               "to": f'{end.isoformat()}Z'},
                "filter": filter_tsx,
                "take": 250000,
                "projectedProperties": [{'name': v.name,
                                         'type': v.var_value_tsx.split('.')[-1]}
                                        for v in variables]
            }
        }

        # Retrieve the DataFrame for the Time Series vars
        return self._get_time_data(payload=payload,
                                   use_warm_store=use_warm_store,
                                   drop_nans=drop_nans)

    def get_series(self, start, end, variables=None,
                   filter_tsx=None, use_warm_store=False,
                   drop_nans=False, resolve_categories=True):
        """
        Retrieve time series of calculated variable values from events

        This method will return the series data for the given timespan.
        This method is different from `get_events` because `get_events`
        can only retrieve events as sent to the TSI, whereas this method
        will also return computed series (the log of a series of events
        or two series summed).

        Please note that the API is limited to 250000 events.

        More information:
            https://docs.microsoft.com/en-us/rest/api/time-series-insights/dataaccessgen2/query/execute#getseries

        Parameters
        ----------
        start : datetime.datetime
                Initial instant
        end : datetime.datetime
              Final instant
        variables : list [ NumericVariable ] or None, optional
                    Variables whose data should be retrieved for the given
                    time series instances. The variable definitions need
                    not exist in the TSI, but their tsx must be compatible
                    with the time series.

                    If not provided, all the variables for the type associated
                    with this time series will be fetched.
        filter_tsx : str, optional
                     Top-level filter string, can be None.
        use_warm_store : bool
                         Flag indicating whether the warm store shouldbe used.
        drop_nans : bool
                    Flag indicating whether rows of data that are only filled
                    with NaNs should be dropped from the returned DataFrame or
                    whether data should be returned exactly as provided by the
                    TSI.
        resolve_categories : bool, optional
                             Convert raw data from categorical variables into
                             categorical series in the DataFrame. Set this to
                             `False` to retrieve the raw data from the TSI
                             for categorical variables.

        Returns
        -------
        pd.DataFrame
            Events for the given timespan, merged into a single DataFrame.
        """
        if variables is None:
            variables = self.series_type.vars
        if start >= end:
            raise ValueError('End time must be greater than start time')
        if start.tzinfo is not None:
            start = start.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        if end.tzinfo is not None:
            end = end.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        # The payload we'll use for requesting data from the TSI
        payload = {
            'getSeries': {
                'timeSeriesId': self.series_id,
                'searchSpan': {"from": f'{start.isoformat()}Z',
                               "to": f'{end.isoformat()}Z'},
                'filter': filter_tsx,
                'take': 250000,
                "projectedVariables": [ts_var.name for ts_var in variables],
                'inlineVariables': {var_name: body
                                    for ts_var in variables
                                    for var_name, body in ts_var.as_dict().items()}
            }
        }

        # Retrieve the DataFrame for the Time Series vars
        data = self._get_time_data(payload=payload,
                                   use_warm_store=use_warm_store,
                                   drop_nans=drop_nans)

        # Convert categorical data into actual categorical variables
        # This can probably be optimized...
        if resolve_categories:
            for var in variables:
                if var.kind == 'categorical':
                    categories = []
                    mask = None
                    # Set normal categories
                    for category in var.categories:
                        category_mask = data[var.name].isin(category.values)
                        data.loc[category_mask, var.name] = category.label
                        categories.append(category.label)
                        if mask is None:
                            mask = category_mask
                        else:
                            mask |= category_mask
                    # Set default categories
                    data.loc[(~mask & ~data[var.name].isna()), var.name] = var.default_category.label
                    categories.append(var.default_category.label)
                    data[var.name] = pd.Categorical(data[var.name], categories=categories)

        return data

    def aggregate_series(self, start, end, interval, variables=None,
                         filter_tsx=None, use_warm_store=False,
                         drop_nans=False, resolve_categories=True):
        """
        Retrieve an aggregation of time series

        This method will return the series data for the given timespan.
        This is different from `get_events` & `get_series` because this
        method can aggregate data.

        Please note that the API is limited to 250000 events.

        More information:
            https://docs.microsoft.com/en-us/rest/api/time-series-insights/dataaccessgen2/query/execute#aggregateseries

        Parameters
        ----------
        start : datetime.datetime
                Initial instant
        end : datetime.datetime
              Final instant
        interval : str
                   Interval size between outputs, given in ISO-8601 format.
                   For example: `PT1S` corresponds to an interval of 1 second
                   and `PT1M` corresponds to an interval of 1 minute.
        variables : list [ NumericVariable ]
                    Variables whose data should be retrieved for the given
                    time series instances. The variable definitions need
                    not exist in the TSI, but their tsx must be compatible
                    with the time series.
        filter_tsx : str, optional
                     Top-level filter string, can be None.
        use_warm_store : bool
                         Flag indicating whether the warm store shouldbe used.
        drop_nans : bool
                    Flag indicating whether rows of data that are only filled
                    with NaNs should be dropped from the returned DataFrame or
                    whether data should be returned exactly as provided by the
                    TSI.
        resolve_categories : bool, optional
                             Convert raw data from categorical variables into
                             categorical series in the DataFrame. Set this to
                             `False` to retrieve the raw data from the TSI
                             for categorical variables.

        Returns
        -------
        pd.DataFrame
            Events for the given timespan, merged into a single DataFrame.
        """
        if variables is None:
            variables = self.series_type.vars
        if start >= end:
            raise ValueError('End time must be greater than start time')
        if start.tzinfo is not None:
            start = start.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        if end.tzinfo is not None:
            end = end.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        # The payload we'll use for requesting data from the TSI
        payload = {
            'aggregateSeries': {
                'timeSeriesId': self.series_id,
                'searchSpan': {"from": f'{start.isoformat()}Z',
                               "to": f'{end.isoformat()}Z'},
                'filter': filter_tsx,
                "projectedVariables": [ts_var.name for ts_var in variables],
                'inlineVariables': {var_name: body
                                    for ts_var in variables
                                    for var_name, body in ts_var.as_dict().items()},
                'take': 250000,
                'interval': interval
            }
        }

        # Retrieve the DataFrame for the Time Series vars
        data = self._get_time_data(payload=payload,
                                   use_warm_store=use_warm_store,
                                   drop_nans=drop_nans)

        # Convert categorical data into actual categorical variables
        # This can probably be optimized...
        if resolve_categories:
            for var in variables:
                if var.kind == 'categorical':
                    categories = []
                    mask = None
                    # Set normal categories
                    for category in var.categories:
                        category_mask = data[var.name].isin(category.values)
                        data.loc[category_mask, var.name] = category.label
                        categories.append(category.label)
                        if mask is None:
                            mask = category_mask
                        else:
                            mask |= category_mask
                    # Set default categories
                    data.loc[(~mask & ~data[var.name].isna()), var.name] = var.default_category.label
                    categories.append(var.default_category.label)
                    data[var.name] = pd.Categorical(data[var.name], categories=categories)

        return data

    def _get_time_data(self, payload, use_warm_store, drop_nans=True):
        """
        Helper method used for performing the query to the TSI

        This method will perform the query with the given payload
        and handle low-level tasks like pagination & converting
        the information returned by the server in JSON format into
        a Pandas DataFrame.

        Parameters
        ----------
        payload : dict
                  Dictionary with the request payload
        use_warm_store : bool
                         Flag indicating whether the warm store should
                         be used for the query.
        drop_nans: bool
                   Flag indicating whether rows composed of only
                   NaNs should be discarded from the returned DataFrame.

        Returns
        -------
        pd.DataFrame
                    The information provided by the TSI, in DataFrame format.
        """
        # Query params
        url = f'https://{environment.ENVIRONMENT_ID}.env.timeseries.azure.com/timeseries/query?'
        querystring = get_query_string(use_warm_store=use_warm_store)
        authorization_token = get_authorization_token()
        headers = {
            "x-ms-client-application-name": environment.APPLICATION_NAME,
            "Authorization": authorization_token,
            "Content-Type": "application/json",
            "cache-control": "no-cache",
        }

        # Perform the query & handle paging
        try:
            r = requests.request("POST",
                                 url,
                                 data=json.dumps(payload),
                                 headers=headers,
                                 params=querystring)
            r.raise_for_status()
        except requests.exceptions.ConnectTimeout:
            logging.error("pyTSI: The request to the TSI API timed out.")
            raise
        except requests.exceptions.HTTPError:
            logging.error("pyTSI: The request to the TSI API returned "
                          "an unsuccessful status code.")
            raise

        # Construct the dictionary we'll use for the DataFrame
        json_data = r.json()
        df_data = {'timestamp': json_data['timestamps']}
        for p in json_data['properties']:
            df_data[p['name']] = p['values']

        # Handle the pagination token, untested
        while 'continuationToken' in json_data.keys():
            headers['x-ms-continuation'] = json_data['continuationToken']
            r = requests.request('POST',
                                 url,
                                 data=json.dumps(payload),
                                 headers=headers,
                                 params=querystring)
            r.raise_for_status()

            if r.text:
                json_data = r.json()
                df_data['timestamp'].extend(json_data['timestamps'])
                for p in json_data['properties']:
                    df_data[p['name']].extend(p['values'])

        # Construct the DataFrame from the info we just received
        df = pd.DataFrame.from_dict(df_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp').sort_index()

        if drop_nans:
            df = df.dropna(how='all')

        return df

    def __repr__(self):
        if len(self.series_id) == 1:
            return f'<Time Series Instance with ID {self.series_id} ' \
                   f'({self.description}) of type ' \
                   f'`{self.series_type.name}`>'
        else:
            return f'<Time Series Instance with IDs {self.series_id} ' \
                   f'({self.description}) of type ' \
                   f'`{self.series_type.name}`>'
