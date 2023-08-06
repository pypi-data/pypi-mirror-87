import os

import numpy
import pandas
from numpy.testing import assert_array_equal
from pandas.testing import assert_frame_equal, assert_series_equal

from tests.integration.samples.endpoints import tktl
from tktl.core.clients.arrow import ArrowFlightClient


def test_fetch_data():
    k = os.environ["TEST_USER_API_KEY"]
    client = ArrowFlightClient(api_key=k, repository_name="test", local=True)
    for endpoint in tktl.endpoints:
        client.authenticate(endpoint_name=f"{endpoint.func.__name__}")
        x, y = client.get_sample_data()
        assert_data_equals(x, endpoint.input_schema.value)
        assert_data_equals(y, endpoint.output_schema.value)


def assert_data_equals(left, right):
    assert type(left) == type(right)
    if isinstance(left, pandas.DataFrame):
        assert_frame_equal(left, right)
    elif isinstance(left, pandas.Series):
        assert_series_equal(left, right, check_names=False)
    elif isinstance(left, numpy.ndarray):
        assert_array_equal(left, right)
    else:
        raise
