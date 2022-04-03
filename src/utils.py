import random
from loguru import logger


class ProxyManager:
    _proxies: list = []

    def __init__(self, proxies: list):
        self._proxies = self._set_proxies(proxies)

    def _set_proxies(self, proxies: list):
        _proxies = []
        for i in proxies:
            _proxies.append({"https": i})

        logger.info("Found {} proxies", len(proxies))
        return _proxies

    def random(self):
        random_proxy = None

        if self._proxies:
            random_proxy = self._proxies[random.randint(0, len(self._proxies) - 1)]
        return random_proxy
