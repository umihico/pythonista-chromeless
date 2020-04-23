# chromeless
AWS lambda & selenium & python is powerful solution.  
Let's access this benefit easily!

+ Don't create lambda every time. Just create this once.
+ Write the method and send it through API.
+ Selenium dynamically execute your script.

## Example
```python
# Write the method
def get_title(self, url):
    self.get(url)
    return self.title

# Prepare your credentials
gateway_url = "https://XXXXXXXXXX.execute-api.us-west-2.amazonaws.com/default/chromeless"
gateway_apikey = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Attach the method and call it.
from chromeless import Chromeless
chrome = Chromeless(gateway_url, gateway_apikey)
chrome.attach_method(get_title)
print(chrome.get_title("https://google.com")) # Google
```

## Installing
1. AWS environment
    + clone this repository and `cd sls`
    + `serverless deploy` and note the url and apikey
2. Local environment
    + `pip install chromeless`
    + `cd sls`
    + replace dummy credentials in `test.py` for test use

That's it! Now run the `test.py` or custom as you want!

## Tips
+ **One call, One instance.** Solution is wrapping.  

```python
# BAD EXAMPLE
chrome = Chromeless(awsgateway_url, awsgateway_apikey)
chrome.get("https://google.com") # Lambda get triigered here.
chrome.save_screenshot("screenshot.png") # So any following methods are rejected.

# SOLUTION
def wrapper(self,url,filename):
    self.get(url)
    self.save_screenshot(filename)

chrome = Chromeless(awsgateway_url, awsgateway_apikey)
chrome.attach_method(wrapper)
chrome.wrapper("https://google.com","screenshot.png")
```

+ You can set chrome_options to change window resolution

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
