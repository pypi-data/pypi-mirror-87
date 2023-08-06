from tests.integration.samples import tktl
from tktl.core.t import EndpointKinds


def test_this():
    assert len(tktl.endpoints) == 7


def test_profiling_enabled():
    for e in tktl.endpoints[0:6]:
        if e.KIND.value == EndpointKinds.CUSTOM.value:
            assert e.profiling_supported is False
        else:
            assert e.profiling_supported is True
    assert tktl.endpoints[-1].profiling_supported is False


def test_app_runs():
    ...
