import abc

from tktl.core.clients import TaktileClient
from tktl.core.clients.arrow import ArrowFlightClient
from tktl.core.clients.rest import RestClient
from tktl.core.config import settings
from tktl.core.managers.auth import AuthConfigManager
from tktl.core.t import ServiceT


class CommandBase(object):
    def __init__(self, api=None):
        self.api = api


class BaseClientCommand:
    def __init__(
        self,
        kind: ServiceT,
        api_key: str,
        repository: str,
        branch_name: str,
        local: bool = False,
    ):
        self.kind = kind
        self.client_params = {
            "api_key": api_key,
            "repository_name": repository,
            "branch_name": branch_name,
            "local": local,
        }
        self.client = self._get_client()

    def execute(self, *args, **kwargs):
        pass

    def _get_client(self):
        return (
            RestClient(**self.client_params)
            if self.kind == ServiceT.REST.value
            else ArrowFlightClient(**self.client_params)
        )


class BaseApiCommand:
    __metaclass__ = abc.ABCMeta

    def __init__(
        self, api_url=settings.DEPLOYMENT_API_URL,
    ):
        self.api_url = api_url
        self.client = self._get_client()

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def _get_client(self):
        return TaktileClient(api_url=self.api_url)


class BaseDeploymentApiCommand(BaseApiCommand):
    def __init__(self):
        super().__init__(api_url=settings.DEPLOYMENT_API_URL)

    def execute(self, *args, **kwargs):
        raise NotImplementedError


class BaseTaktileApiCommand(BaseApiCommand):
    def __init__(self):
        super().__init__(api_url=settings.TAKTILE_API_URL)

    def execute(self, *args, **kwargs):
        raise NotImplementedError


class BaseRestClientCommand(BaseClientCommand):
    def __init__(self, repository: str, branch_name: str, local: bool):
        super().__init__(
            kind=ServiceT.REST.value,
            api_key=AuthConfigManager.get_api_key(),
            repository=repository,
            branch_name=branch_name,
            local=local,
        )


class BaseGrpcClientCommand(BaseClientCommand):
    def __init__(self, repository: str, branch_name: str, local: bool):
        super().__init__(
            kind=ServiceT.GRPC.value,
            api_key=AuthConfigManager.get_api_key(),
            repository=repository,
            branch_name=branch_name,
            local=local,
        )
