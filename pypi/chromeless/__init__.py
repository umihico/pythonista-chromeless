__all__ = ["Chromeless", ]

from .dump_code import dump_code
import requests
import types


class Chromeless():
    def __init__(self, gateway_url, apikey):
        self.gateway_url = gateway_url
        self.headers = {"x-api-key": apikey}

    def attach_method(self, func):
        def method(self, *arg, **kwargs):
            arg = arg or tuple()
            kwargs = kwargs or dict()
            return self._run_method(func, arg, kwargs)
        setattr(self, func.__name__, types.MethodType(method, self))

    def _run_method(self, func, arg, kwargs):
        data = dump_code(func, arg, kwargs)
        response = requests.post(self.gateway_url, data=data, headers=self.headers)
        body = response.text
        return body
