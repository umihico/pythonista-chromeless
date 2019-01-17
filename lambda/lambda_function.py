from selenium.webdriver import Chrome, ChromeOptions
import json


def lambda_handler(event, context):
    options = ChromeOptions()
    options.binary_location = "./bin/headless-chromium"
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--homedir=/tmp")
    driver = Chrome("./bin/chromedriver", chrome_options=options)
    driver.get("https://www.google.co.jp")
    title = driver.title
    driver.quit()
    print(title)
    text = f'Hello from Lambda!{title}'
    return {
        'statusCode': 200,
        'body': json.dumps(text)
    }
