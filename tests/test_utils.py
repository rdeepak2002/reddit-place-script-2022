import pytest
from faker import Faker
from random import randint

from src.utils import ProxyManager


@pytest.fixture(autouse=True, scope="class")
def fake():
    yield Faker()


class TestProxy:

    def test_proxies_init(self, fake):
        # Arrange
        proxies = [fake.ipv4() for _ in range(randint(1, 10))]

        # Act
        manager = ProxyManager(proxies)

        # Assert
        assert isinstance(manager._proxies, list)
        assert len(manager._proxies) == len(proxies)
        assert manager._proxies == [{"https": proxy} for proxy in proxies]

    def test_random_proxy(self, fake):
        # Arrange
        proxies = [fake.ipv4() for _ in range(randint(1, 10))]
        manager = ProxyManager(proxies)

        # Act
        random_proxy = manager.random()

        # Assert
        assert isinstance(random_proxy, dict)
        assert random_proxy in manager._proxies
