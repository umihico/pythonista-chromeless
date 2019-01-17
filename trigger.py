GATEWAY_URL = "https://7wsebamsma.execute-api.us-west-2.amazonaws.com/default/serverless-plain-selenium"
from apikey import apikey
import urllib.request
import json


def trigger(method='GET', data=None):
    data = data or json.dumps(data).encode()
    headers = {"x-api-key": apikey}
    req = urllib.request.Request(GATEWAY_URL, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=29) as res:
        body = res.read()
    return body


if __name__ == '__main__':
    print(trigger())
