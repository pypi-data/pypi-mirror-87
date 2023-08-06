import os
from .environment import environment
from .environment.environment_api import EnvironmentApi
from .hierarchies.hierarchies_api import HierarchiesApi
from .instances.TimeSeries import TimeSeries
from .instance_types.Types import Types


class TSIClient:
    """TSIClient. Holds methods to interact with an Azure TSI environment.

    This class can be used to retrieve time series data from Azure TSI. Data
    is retrieved in form of a pandas dataframe, which allows subsequent analysis
    by data analysts, data scientists and developers.

    It can be instantiated either by arguments or by environment variables (if arguments
    are specified, they take precedence even when environment variables are set).

    Args:
        environment_name (str): The name of the Azure TSI environment.
        client_id (str): The client id of the service principal used to authenticate with Azure TSI.
        client_secret (str): The client secret of the service principal used to authenticate with Azure TSI.
        tenant_id (str): The tenant id of the service principal used to authenticate with Azure TSI.
        application_name (str): The name can be an arbitrary string. For informational purpose.
        api_version (str): The TSI api version (optional, allowed values: '2018-11-01-preview' and '2020-07-31').
            Defaults to '2020-07-31'.

    Examples:
        The TSIClient is the entry point to the SDK. You can instantiate it like this:

            >>> from pyTSI import TSIClient as TSI
            >>> client = TSI.TSIClient(
            ...     environment="<your-tsi-env-name>",
            ...     client_id="<your-client-id>",
            ...     client_secret="<your-client-secret>",
            ...     tenant_id="<your-tenant-id>",
            ...     applicationName="<your-app-name>">,
            ...     api_version="2020-07-31"
            ... )

        You might find it useful to specify environment variables to instantiate the TSIClient.
        To do so, you need to set the following environment variables:

        * ``PYTSI_APPLICATION_NAME``
        * ``PYTSI_ENVIRONMENT_NAME``
        * ``PYTSI_CLIENT_ID``
        * ``PYTSI_CLIENT_SECRET``
        * ``PYTSI_TENANT_ID``
        * ``TSI_API_VERSION``
        
        Now you can instantiate the TSIClient without passing any arguments:

            >>> from pyTSI import TSIClient as TSI
            >>> client = TSI.TSIClient()
    """

    def __init__(
            self,
            environment_name=None,
            client_id=None,
            client_secret=None,
            application_name=None,
            tenant_id=None,
            api_version=None
    ):
        self._application_name = application_name if application_name is not None else os.environ[
            "PYTSI_APPLICATION_NAME"]
        environment_name = environment_name if environment_name is not None else os.environ[
            "PYTSI_ENVIRONMENT_NAME"]
        client_id = client_id if client_id is not None else os.environ["PYTSI_CLIENT_ID"]
        client_secret = client_secret if client_secret is not None else os.environ["PYTSI_CLIENT_SECRET"]
        tenant_id = tenant_id if tenant_id is not None else os.environ["PYTSI_TENANT_ID"]

        allowed_api_versions = ['2020-07-31', '2018-11-01-preview']
        if api_version in allowed_api_versions:
            api_version = api_version
        elif 'TSI_API_VERSION' in os.environ:
            if os.environ['TSI_API_VERSION'] in allowed_api_versions:
                api_version = os.environ['TSI_API_VERSION']
        else:
            api_version = '2020-07-31'

        # Configure the environment, this limits us to a connection to a single TSI
        environment.CLIENT_ID = client_id
        environment.CLIENT_SECRET = client_secret
        environment.TENANT_ID = tenant_id
        environment.API_VERSION = api_version
        environment.APPLICATION_NAME = self._application_name
        environment.ENVIRONMENT_NAME = environment_name

        self.environment = EnvironmentApi()
        environment.ENVIRONMENT_ID = self.environment.get_environment_id()

        self.hierarchies = HierarchiesApi()
        self.types = Types()
        self.time_series = TimeSeries(types=self.types)
