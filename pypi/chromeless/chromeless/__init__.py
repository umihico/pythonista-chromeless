__all__ = ["Chromeless", "dump_codes"]

from .client_pickler import dump_codes, unpickle_result
from .screenshot_client import exact_result_and_save_screenshots
import requests
import types
import io
from PIL import Image


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

    def _main_method_handler(self, *arg, **kwargs):
        arg = arg or tuple()
        kwargs = kwargs or dict()
        data = dump_codes(self.called_name_as_method, arg, kwargs, self.stored_funcs)
        response = requests.post(self.gateway_url, data=data, headers=self.headers)
        body = response.text
        result = unpickle_result(body)
        result = exact_result_and_save_screenshots(result)
        return result

    def save_screenshot_binary(self, filename, binarydata):
        img = Image.open(io.BytesIO(binarydata))
        img.save(filename)
