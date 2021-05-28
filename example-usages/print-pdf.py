from chromeless import Chromeless
import base64


def print_pdf(self, url):
    self.get(url)
    import json
    resource = "/session/%s/chromium/send_command_and_get_result" % self.session_id
    url = self.command_executor._url + resource
    body = json.dumps({'cmd': "Page.printToPDF", 'params': {}})
    response = self.command_executor._request('POST', url, body)
    return response.get('value')['data']


if __name__ == '__main__':
    chrome = Chromeless()
    chrome.attach(print_pdf)
    url = "https://github.com/umihico/pythonista-chromeless"
    data = chrome.print_pdf(url)
    with open("result.pdf", 'wb') as file:
        file.write(base64.b64decode(data))
