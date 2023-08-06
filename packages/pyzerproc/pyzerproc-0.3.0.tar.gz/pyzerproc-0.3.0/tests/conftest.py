import pytest


@pytest.fixture
def adapter(mocker):
    return mocker.patch('pygatt.GATTToolBackend')()


@pytest.fixture
def device(mocker, adapter):
    device = mocker.Mock()
    adapter.connect.return_value = device
    return device
