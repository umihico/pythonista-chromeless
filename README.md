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
+ create one AWS lambda fuction
+ select [Code entry type] and [Upload a .ZIP file]
+ upload awslambda/deploy_package.zip
+ increase capacity of lambda. 3 seconds is not enough
+ create and attach AWS API Gateway and note the url and apikey
+ `pip install chromeless`
+ write and run your method
