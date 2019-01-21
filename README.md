# chromeless
AWS lambda unit which execute given code on selenium

## Example
```python
# write the code as method of selenium.webdriver.Chrome
def get_title(self, url):
    self.get(url)
    return self.title

# prepare your credentials
gateway_url = "https://XXXXXXXXXX.execute-api.us-west-2.amazonaws.com/default/chromeless"
gateway_apikey = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Then attach the function and just call it.
from chromeless import Chromeless
chrome = Chromeless(gateway_url, gateway_apikey)
chrome.attach_method(get_title)
chrome.get_title("https://google.com") # Google
```

## Installing
1. AWS environment
    + Create new lambda function
    + Select [Code entry type] and [Upload a .ZIP file]
    + Upload [deploy_package.zip](https://github.com/umihico/chromeless/blob/master/awslambda/deploy_package.zip)
    + Increase the timeout setting and the memory setting enough
    + Create API Gateway for this lambda and note the url and apikey
2. Local environment
    + `pip install chromeless`
    + download [examples.py](https://github.com/umihico/chromeless/blob/master/examples.py)
    + put your credentials as `awsgateway_apikey` and `awsgateway_url` in examples.py

That's it! Now run the examples.py and change it as you want!

## Tips
+ **One call, One instance.** Solution is wrapping.  

```python
# BAD EXAMPLE
chrome = Chromeless(awsgateway_url, awsgateway_apikey)
chrome.get("https://google.com") # lambda get triigered here
chrome.save_screenshot("screenshot.png") # so next method won't work

# SOLUTION
def wrapper(self,url,filename):
    self.get(url)
    self.save_screenshot(filename)

chrome = Chromeless(awsgateway_url, awsgateway_apikey)
chrome.attach_method(wrapper)
chrome.wrapper("https://google.com","screenshot.png")
```

+ you can set chrome_options to change window resolution

```python
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
# chrome_options.add_argument("--window-size=1280x1696") # DEFAULT
chrome_options.add_argument("--disable-application-cache")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--hide-scrollbars")
chrome_options.add_argument("--enable-logging")
chrome_options.add_argument("--log-level=0")
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--homedir=/tmp")
chrome = Chromeless(awsgateway_url, awsgateway_apikey, chrome_options=chrome_options)
```
