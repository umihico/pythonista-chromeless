from trigger import trigger, dump_code, load_code
import types
from selenium.webdriver import Chrome, ChromeOptions


def method(self):
    self.get("https://www.google.co.jp")
    title = self.title
    self.quit()
    return title


def test_local_binding(sended_method):
    Chrome.sended_method = sended_method
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome = Chrome(chrome_options=chrome_options)
    print(chrome.sended_method())


def main():
    sended_method = load_code(dump_code(method))
    test_local_binding(sended_method)
    print(trigger(method="POST", func=method))


if __name__ == '__main__':
    main()
