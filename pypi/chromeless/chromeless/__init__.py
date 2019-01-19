__all__ = ["Chromeless", "dump_codes"]

from .client_pickler import dump_codes, unpickle_result
import requests
import types


class Chromeless():
    def __init__(self, gateway_url, apikey):
        self.gateway_url = gateway_url
        self.headers = {"x-api-key": apikey}
        self.stored_funcs = {}

    def attach_method(self, func):
        self.stored_funcs[func.__name__] = func

    def __getattr__(self, methodname):
        "this is the main method"
        self.called_name_as_method = methodname
        return self._main_method_handler
        #
        #
        # def method(self, *arg, **kwargs):
        #     arg = arg or tuple()
        #     kwargs = kwargs or dict()
        #     return self._main_method(func, arg, kwargs)
        # setattr(self, func.__name__, types.MethodType(method, self))

    def _main_method_handler(self, *arg, **kwargs):
        arg = arg or tuple()
        kwargs = kwargs or dict()
        data = dump_codes(self.called_name_as_method, arg, kwargs, self.stored_funcs)
        response = requests.post(self.gateway_url, data=data, headers=self.headers)
        body = response.text
        return unpickle_result(body)
