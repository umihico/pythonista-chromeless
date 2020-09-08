# chromeless
AWS lambda & selenium & python is powerful solution.  
Let's access this benefit easily!

+ Don't create lambda functions every time. Just create this once.
+ Write the method.
+ Selenium dynamically execute your script.

## Example
```python
# Write the method
def get_title(self, url):
    self.get(url)
    return self.title

# Attach the method and call it.
from chromeless import Chromeless
chrome = Chromeless()
chrome.attach(get_title)
print(chrome.get_title("https://google.com")) # Google
```

## Installing
1. AWS environment (AWS CLI is required)
    + `docker run -e AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id) -e AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key) -e AWS_DEFAULT_REGION=$(aws configure get region) umihico/chromelessenv`

2. Local environment
    + `pip install chromeless`

That's it! Now run the `example.py` and confirm it works!

## Tips
+ **Only one method is attachable.** Solution is wrapping.

```python
# BAD EXAMPLE
chrome = Chromeless()
chrome.get("https://google.com") # Not attached method. AttributeError will be raised.
chrome.title # Same. AttributeError.

# SOLUTION
def wrapper(self, url):
    self.get(url)
    return self.title

chrome = Chromeless()
chrome.attach(wrapper) # You can attach only one method
print(chrome.wrapper("https://google.com")) # prints 'Google'
print(chrome.wrapper("https://microsoft.com")) # But you can execute as many times as you want.
print(chrome.wrapper("https://apple.com")) # Arguments are adjustable each time.
```

+ To screenshot

```python
# BAD EXAMPLE
def bad_wrapper(self):
  self.get("https://google.com")
  self.save_screenshot("screenshot.png")
  # There's no sense in saving files in AWS Lambda

# SOLUTION
def good_wrapper(self):
  self.get("https://google.com")
  return self.get_screenshot_as_png()
  # return image as binary data.

chrome = Chromeless()
chrome.attach(good_wrapper)
png = chrome.good_wrapper()
# then write image down locally
with open("screenshot.png", 'wb') as f:
    f.write(png)

```
