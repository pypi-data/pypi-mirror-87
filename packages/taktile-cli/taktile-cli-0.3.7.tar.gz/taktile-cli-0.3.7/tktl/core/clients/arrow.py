from concurrent.futures.thread import ThreadPoolExecutor

from pyarrow import Table
from pyarrow.flight import (
    ClientAuthHandler,
    FlightCancelledError,
    FlightClient,
    FlightDescriptor,
    FlightInfo,
    FlightUnauthenticatedError,
    FlightUnavailableError,
    Ticket,
)

from tktl.core.clients import Client
from tktl.core.config import settings
from tktl.core.exceptions import AuthenticationError
from tktl.core.exceptions.exceptions import APIClientException
from tktl.core.loggers import LOG, Logger
from tktl.core.schemas.repository import _format_grpc_url, load_certs
from tktl.core.serializers import deserialize_arrow, serialize_arrow
from tktl.core.t import ServiceT


class ApiKeyClientAuthHandler(ClientAuthHandler):
    """An example implementation of authentication via ApiKey."""

    def __init__(self, api_key: str):
        super(ApiKeyClientAuthHandler, self).__init__()
        self.api_key = api_key

    def authenticate(self, outgoing, incoming):
        outgoing.write(self.api_key)
        self.api_key = incoming.read()

    def get_token(self):
        return self.api_key


class ArrowFlightClient(Client):
    TRANSPORT = ServiceT.GRPC

    def __init__(
        self,
        api_key: str,
        repository_name: str,
        branch_name: str = None,
        local: bool = False,
        logger: Logger = LOG,
    ):
        super().__init__(
            api_key=api_key,
            repository_name=repository_name,
            branch_name=branch_name,
            local=local,
            logger=logger,
        )

    @staticmethod
    def format_url(url: str) -> str:
        return _format_grpc_url(url)

    @property
    def local_endpoint(self):
        return settings.LOCAL_ARROW_ENDPOINT

    def list_deployments(self):
        pass

    def list_commands(self):
        return self.client.list_actions()

    def authenticate(self, endpoint_name: str):
        location = self.get_endpoint_and_location(endpoint_name)
        if not location:
            return
        certs = load_certs()
        client = FlightClient(tls_root_certs=certs, location=location)
        self.logger.trace(f"Performing authentication request against {location}")
        client.authenticate(
            ApiKeyClientAuthHandler(api_key=self.taktile_client.api_key)
        )
        self.set_client_and_location(location=location, client=client)

    def predict(self, inputs):
        table = serialize_arrow(inputs)
        descriptor = self.get_flight_info(command_name=str.encode(self.endpoint))
        writer, reader = self.client.do_exchange(descriptor.descriptor)
        self.logger.trace(f"Initiating prediction request")
        with writer:
            writer.begin(table.schema)
            writer.write_table(table)
            writer.done_writing()
            table = reader.read_all()
            return deserialize_arrow(table)

    def get_sample_data(self):
        if not self.endpoint:
            raise AuthenticationError(
                "Please authenticate against a specific endpoint first"
            )
        x_ticket, y_ticket = (
            str.encode(f"{self.endpoint}__X"),
            str.encode(f"{self.endpoint}__y"),
        )
        return self._get_data(ticket=x_ticket), self._get_data(ticket=y_ticket)

    def _get_data(self, ticket):
        if not self.endpoint:
            raise AuthenticationError(
                "Please authenticate against a specific endpoint first"
            )
        self.logger.trace(f"Fetching sample data from server")
        reader = self.client.do_get(Ticket(ticket=ticket))
        with ThreadPoolExecutor() as executor:
            future = executor.submit(blocking_read, reader)
            return_value = future.result()
            return deserialize_arrow(return_value)

    def get_schema(self):
        if not self.endpoint:
            raise AuthenticationError(
                "Please authenticate against a specific endpoint first"
            )
        info = self.get_flight_info(str.encode(self.endpoint))
        return info.schema

    def get_flight_info(self, command_name: bytes) -> FlightInfo:
        descriptor = FlightDescriptor.for_command(command_name)
        return self.client.get_flight_info(descriptor)

    def health(self):
        try:
            self.logger.trace(f"Connecting to server...")
            self.client.wait_for_available(timeout=1)
        except FlightUnauthenticatedError:
            self.logger.trace(f"Connection successful")
            return True
        except (FlightCancelledError, FlightUnavailableError):
            raise APIClientException(
                detail="Arrow flight is unavailable", status_code=502
            )
        return True


def blocking_read(reader):
    batches = []
    while True:
        try:
            batch, metadata = reader.read_chunk()
            batches.append(batch)
        except StopIteration:
            break
    return Table.from_batches(batches)
