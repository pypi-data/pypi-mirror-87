import json
import logging
import requests
import functools

from pyrasgo.version import __version__ as pyrasgo_version
from pyrasgo.session import Environment

PRODUCTION_HEAP_KEY = '540300130'
STAGING_HEAP_KEY = '3353132567'

HEAP_URL = "https://heapanalytics.com/api"
# HEAP_PROPS_URL = f"{HEAP_URL}/add_user_properties"


def track_usage(func):
    @functools.wraps(func)
    def decorated(self, *args, **kwargs):
        try:
            self._api_key
        except AttributeError:
            logging.debug(f"Cannot track functions called from {self.__class__.__name__} class.")
            return func(self, *args, **kwargs)

        if self._environment == Environment.LOCAL:
            logging.info(f"Called {func.__name__} with parameters: {kwargs}")
        else:
            try:
                track_call(
                    app_id=PRODUCTION_HEAP_KEY if self._environment == Environment.PRODUCTION else STAGING_HEAP_KEY,
                    user_id=self._profile.get('user_id', 0),
                    event=func.__name__,
                    properties={"hostname": self._environment.value,
                                "source": "pyrasgo",
                                "class": self.__class__.__name__,
                                "version": pyrasgo_version,
                                "username": self._profile.get('username', 'Unknown'),
                                "input": args,
                                **kwargs})
            except Exception:
                logging.debug(f"Called {func.__name__} with parameters: {kwargs}")
        return func(self, *args, **kwargs)

    return decorated


def track_call(app_id: str,
               user_id: int,
               event: str,
               properties: dict = None):
    """
    Send a "track" event to the Heap Analytics API server.

    :param event: event name
    :param properties: optional, additional event properties
    """
    data = {"app_id": app_id,
            "identity": user_id,
            "event": event}

    if properties is not None:
        data["properties"] = properties

    response = requests.post(url=f"{HEAP_URL}/track",
                             data=json.dumps(data),
                             headers={"Content-Type": "application/json"})
    response.raise_for_status()
    return response
