from typing import Union

from pyarrow._flight import FlightClient

from tktl.core.clients.http_client import API
from tktl.core.clients.taktile import TaktileClient
from tktl.core.clients.utils import get_deployment_from_endpoint_and_branch
from tktl.core.config import settings
from tktl.core.loggers import LOG
from tktl.core.t import ServiceT
from tktl.login import login


class Client(object):
    TRANSPORT: str = ServiceT

    def __init__(
        self,
        api_key: str,
        repository_name: str,
        branch_name: str = None,
        local: bool = False,
    ):
        login(api_key)
        self.local = local
        self.taktile_client = TaktileClient(api_url=settings.DEPLOYMENT_API_URL)
        self.repository_name = repository_name
        self.branch_name = branch_name
        self.logger = LOG
        self._location = None
        self._endpoint = None
        self._client = None

    def local_endpoint(self):
        raise NotImplementedError

    @staticmethod
    def format_url(url: str) -> str:
        raise NotImplementedError

    @property
    def client(self) -> Union[API, FlightClient]:
        return self._client

    @property
    def location(self):
        return self._location

    @property
    def endpoint(self):
        return self._endpoint

    @client.setter
    def client(self, client: Union[API, FlightClient]):
        self._client = client

    @location.setter
    def location(self, value):
        self._location = value

    @endpoint.setter
    def endpoint(self, value):
        self._endpoint = value

    def predict(self, *args, **kwargs):
        raise NotImplementedError

    def set_client_and_location(self, location: str, client: Union[API, FlightClient]):
        self.location = location
        self.client = client

    def get_endpoint_and_location(self, endpoint_name: str):
        self.endpoint = endpoint_name
        if self.local:
            location = self.local_endpoint
        else:
            location = self._get_endpoint_location()
            if not location:
                return
            location = self.format_url(location.public_docs_url)
        return location

    def _get_endpoint_location(self):
        endpoint_mapping = self.taktile_client.get_endpoints_for_repository(
            repository=self.repository_name
        )
        filtered_by_user = get_deployment_from_endpoint_and_branch(
            endpoint_mapping=endpoint_mapping,
            endpoint_name=self.endpoint,
            branch_name=self.branch_name,
        )
        if not filtered_by_user:
            return
        return filtered_by_user

    def list_deployments(self):
        raise NotImplementedError

    def get_sample_data(self):
        raise NotImplementedError

    def get_schema(self, *args, **kwargs):
        raise NotImplementedError

    def health(self):
        raise NotImplementedError
