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
+ if you wanna take screenshot, submit as one method like this  

```python
def get_screenshot(self,url,filename):
    self.get(url)
    self.save_screenshot(filename)
```
