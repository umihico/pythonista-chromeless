import inspect
import marshal
import boto3
import json
from .picklelib import loads, dumps
import sys
import requests
import os


class Chromeless():
    REQUIRED_SERVER_VERSION = 2

    def __init__(self, gateway_url=None, gateway_apikey=None, chrome_options=None, function_name='chromeless-server-prod'):
        self.gateway_url = gateway_url
        self.gateway_apikey = gateway_apikey
        self.options = chrome_options
        if function_name == 'chromeless-server-prod' and 'CHROMELESS_SERVER_FUNCTION_NAME' in os.environ:
            function_name = os.environ['CHROMELESS_SERVER_FUNCTION_NAME']
        self.function_name = function_name
        self.codes = {}

    def attach(self, method):
        self.codes[method.__name__] = inspect.getsource(
            method), marshal.dumps(method.__code__)

    def __getattr__(self, name):
        if name in self.codes:
            self.invoked_func_name = name
            return self.__invoke
        raise AttributeError(
            f"{self.__class__.__name__} object has no attribute {name}")

    def __invoke(self, *arg, **kw):
        dumped = dumps({
            "invoked_func_name": self.invoked_func_name,
            "codes": self.codes,
            "arg": arg,
            "kw": kw,
            "options": self.options,
            "REQUIRED_SERVER_VERSION": self.REQUIRED_SERVER_VERSION,
        })
        if self.function_name == "local":
            method = self.__invoke_local
        elif self.gateway_url is not None:
            method = self.__invoke_api
        else:
            method = self.__invoke_lambda
        response, metadata = loads(method(dumped))
        if metadata['status'] == "error":
            raise Exception(response)
        else:
            return response

    def __invoke_api(self, dumped):
        headers = {'x-api-key': self.gateway_apikey}
        return requests.post(self.gateway_url, headers=headers,
                             json={'dumped': dumped}).json()['result']

    def __invoke_local(self, dumped):
        from server import invoke
        return invoke(dumped)

    def __invoke_lambda(self, dumped):
        client = boto3.client('lambda')
        response = client.invoke(
            FunctionName=self.function_name,
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=json.dumps({'dumped': dumped})
        )
        return response['Payload'].read().decode()
