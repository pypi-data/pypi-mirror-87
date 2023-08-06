# pyTSI

pyTSI is a read-only Python SDK for Microsoft Azure time series insights. 
It provides methods to conveniently retrieve your data and is designed
for analysts, data scientists and developers working with time series 
data in Azure TSI.

The main objective of this library are to:
* Not transform the data in any way. The information will be provided
  to you as delivered by the TSI, gaps and all. The only exception to
  this is that when requesting time series you can ask for rows comprised
  entirely on NaN's to be removed.
* Make it easy and pythonic to obtain the information in the TSI as a
  pandas DataFrame.

Please note that the code is under heavy development and the API will
change frequently and the documentation is not (yet) updated. Also, 
please note that even though this code started as a fork of 
[TSClient](https://github.com/RaaLabs/TSIClient), pyTSI is not compatible
at all with TSIClient.

## Documentation
- Azure time series REST APIs: <https://docs.microsoft.com/en-us/rest/api/time-series-insights/>

## Quickstart
Instantiate the TSIClient to query your TSI environment. Use the credentials 
from your service principal in Azure that has access to the TSI environment 
(you can also use environment variables to instantiate the pyTSI or provide 
a specific TSI API version, check the documentation).

```python
from pyTSI import TSIClient as TSI

client = TSI.TSIClient(environment_name='<your-tsi-env-name>',
                       client_id='<your-client-id>',
                       client_secret='<your-client-secret>',
                       tenant_id='<your-tenant-id>',
                       application_name='<your-app-name>')

# List the instances in the TSI, also list their types
# and variables.
for instance in client.time_series():
    print(f'\t{instance}')
    print('\tInstance type description:')
    print(f'\t\t{instance.series_type}')
    print('\t\tType vars:')
    for v in instance.series_type.vars:
        print(f'\t\t\t{v}')
```

You can now query each instance

You can query your timeseries data by timeseries id, timeseries name or timeseries 
description. The Microsoft TSI apis support aggregation, so you can specify a 
sampling freqency and an aggregation method. Refer to the documentation for detailed 
information.

```python
import datetime

# Define the start & end times for the series that we want to retrieve
t0 = datetime.datetime(year=2020, month=10, day=22, hour=10, minute=53, second=00,
                       tzinfo=datetime.timezone.utc)
t1 = datetime.datetime(year=2020, month=10, day=22, hour=11, minute=53, second=30,
                       tzinfo=datetime.timezone.utc)

# Select a time series by selecting from the list of by filtering by ID
ts = client.time_series.get_by_id(['Time series ID'])
t = ts.series_type
# Get raw event data
raw_events = ts.get_events(start=t0, end=t1, 
                           variables=[t.temperature, t.humidity],
                           drop_nans=True)
# Get series data for raw events & composed variables
series_data = ts.get_series(start=t0, end=t1, 
                            variables=[t.temperature, t.humidity, t.series_sum],
                            drop_nans=True)
# Aggregate series
aggregated_data = ts.aggregate_series(start=t0, end=t1, interval='PT1M', 
                                      variables=[t.temperature, t.EventCount],
                                      drop_nans=True)
```

Each of these functions return a DataFrame, with variable names as columns.

## License
pyTSI is licensed under the MIT license. See [LICENSE](LICENSE.txt) file for details.
