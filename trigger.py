GATEWAY_URL = "https://7wsebamsma.execute-api.us-west-2.amazonaws.com/default/serverless-plain-selenium"
from apikey import apikey
import urllib.request
import json
from awslambda import dump_code, load_code


def trigger(method='GET', func=None):
    if func:
        data = dump_code(func)
    else:
        data = None
    headers = {"x-api-key": apikey}
    req = urllib.request.Request(GATEWAY_URL, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=29) as res:
        body = res.read()
    return body


if __name__ == '__main__':
    # print(trigger())
    print(trigger("POST", trigger))
