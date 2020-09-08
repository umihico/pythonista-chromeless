import inspect
import boto3
import json
from .picklelib import loads, dumps
import sys
import requests


class Chromeless():
    def __init__(self, gateway_url=None, gateway_apikey=None, chrome_options=None, function_name='chromeless-server-prod'):
        self.gateway_url = gateway_url
        self.gateway_apikey = gateway_apikey
        self.options = chrome_options
        self.function_name = function_name

    def attach(self, method):
        self.code = inspect.getsource(method)
        self.name = method.__name__
        setattr(self, self.name, self.__invoke)

    def __invoke(self, *arg, **kw):
        dumped = dumps(
            (self.name, self.code, arg, kw, self.options))
        if self.function_name == "local":
            method = self.__invoke_local
        elif self.gateway_url is not None:
            method = self.__invoke_api
        else:
            method = self.__invoke_lambda
        response = method(dumped)
        try:
            return loads(response)
        except Exception:
            print(response, file=sys.stderr)
            raise

    def __invoke_api(self, dumped):
        headers = {'x-api-key': self.gateway_apikey}
        return requests.post(self.gateway_url, headers=headers,
                             json={'dumped': dumped}).json()['result']

    def __invoke_local(self, dumped):
        from server import ChromelessServer
        return ChromelessServer().recieve(dumped)

    def __invoke_lambda(self, dumped):
        client = boto3.client('lambda')
        response = client.invoke(
            FunctionName=self.function_name,
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=json.dumps({'dumped': dumped})
        )
        return response['Payload'].read().decode()
