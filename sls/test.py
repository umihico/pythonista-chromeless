import requests


def get_credentials():
    import boto3
    ssm = boto3.client('ssm')
    try:
        gateway_domain = ssm.get_parameter(Name='CHROMELESS_TEST_DOMAIN')[
            'Parameter']['Value']
        gateway_apikey = ssm.get_parameter(Name='CHROMELESS_TEST_APIKEY')[
            'Parameter']['Value']
    except Exception:
        gateway_domain = "xxxyyyzzzz.execute-api.xx-yyyy-zz.amazonaws.com"  # PLEASE REPLACE
        gateway_apikey = "xxxxxxYYYYYYzzzzzzXXXXXXXXyyyyyyZZZZZZZZ"  # PLEASE REPLACE
    return gateway_domain, gateway_apikey


def test_selenium():
    """
    test chrome binaries works fine in lambda
    """
    gateway_domain, gateway_apikey = get_credentials()
    gateway_url = f"https://{gateway_domain}/dev/test"
    title = requests.get(gateway_url, headers={
        'x-api-key': gateway_apikey}).json()['title']
    print(title)
    assert title == "Google"


def test_README_example():
    """
    test chromeless pypi package with example function.
    """
    gateway_domain, gateway_apikey = get_credentials()
    gateway_url = f"https://{gateway_domain}/dev/chromeless"

    def get_title(self, url):
        self.get(url)
        return self.title

    from chromeless import Chromeless
    chrome = Chromeless(gateway_url, gateway_apikey)
    chrome.attach_method(get_title)
    title = chrome.get_title("https://google.com")
    print(title)
    assert title == "Google"


if __name__ == '__main__':
    test_selenium()
    test_README_example()
