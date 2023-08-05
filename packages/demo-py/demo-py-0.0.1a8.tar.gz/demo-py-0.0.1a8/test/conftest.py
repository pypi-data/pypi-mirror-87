import pytest
from collections import namedtuple


Config = namedtuple("Config", ["num_to_consume"])


@pytest.fixture(scope="session")
def test_config():
    print("Setup")
    yield Config(
        num_to_consume=10_000
    )
    print("Teardown")
