import os
from enum import Enum
import logging
import requests
from requests.exceptions import HTTPError


def generate_headers(api_key: str) -> dict:
    return {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }


class InvalidApiKeyException(Exception):
    pass


class Environment(Enum):
    PRODUCTION = "api.rasgoml.com"
    STAGING = "staging-rasgo-proxy.herokuapp.com"
    LOCAL = "localhost"

    @classmethod
    def from_environment(cls):
        return cls(os.getenv("RASGO_DOMAIN", cls.PRODUCTION))


class Session(type):
    _api_key = None
    _profile = None
    _environment = None

    def __new__(mcs, name, bases, dct):
        new = super().__new__(mcs, name, bases, dct)
        logging.debug(f'Starting the session for user')
        new._environment = Environment.from_environment()
        new._api_key = mcs._api_key or None
        new._profile = mcs._profile or None
        return new

    def __call__(cls, *args, **kwargs):
        if Session._api_key is None:
            api_key = kwargs.pop("api_key", None)
            if not api_key:
                raise ValueError("Must provide an API key to access the endpoint")
            Session._api_key = api_key
        if Session._environment is None:
            Session._environment = Environment.from_environment()
        if Session._profile is None:
            protocol = 'http' if Session._environment.value == 'localhost' else 'https'
            response = requests.get(
                f"{protocol}://{Session._environment.value}/v1/users/me",
                headers=generate_headers(Session._api_key)
            )
            try:
                response.raise_for_status()
            except HTTPError:
                raise InvalidApiKeyException(f"The API key provided ({Session._api_key[:5]}...{Session._api_key[-5:]}) "
                                             f"is not valid.")
            Session._profile = response.json()
        cls._api_key = Session._api_key
        cls._profile = Session._profile
        cls._environment = Session._environment
        return type.__call__(cls, *args, **kwargs)
