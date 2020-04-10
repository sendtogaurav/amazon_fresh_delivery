# Amazon Fresh Delivery Slot Automated Script

## Usage:
Supports **MacOS, Linux with Chrome**.

The script works on **Chrome** (```amazon_fresh_delivery_slot_chrome.py```). 
It initializes a  webdriver, for which if you don't have one install it from: https://chromedriver.chromium.org/ for Chrome and https://github.com/mozilla/geckodriver/releases for FireFox.

You'll have to update the path of the this installed webdriver under: ```python driver = webdriver.Chrome()``` if its not the default location your OS needs. Similarly, for FireFox ```python driver = webdriver.Firefox(executable_path="<your-webdriver-path>")```


_The script works after you have added all the items to your cart! Note, have your cart ready before running this script! Also, please don't let your computer sleep. Let your computer do the work, while you sleep_

### After you clone the project:

1. Run the requirements.txt (```$ pip install -r requirements.txt```)
2. Run amazon_fresh_delivery_slot_chrome.py 
3. The first time you run this script, amazon will ask you to login. After you login, go to the "Shipping and Payment" window. Its titled: _Schedule your order_. Leave the script running.
4. Once a slot opens the script will verbally notify you of an open slot.
5. Proceed to checkout once you select a time slot. Stay Safe!
