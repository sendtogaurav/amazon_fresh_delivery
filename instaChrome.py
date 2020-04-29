import bs4
from selenium import webdriver

from datetime import datetime,timedelta

from urllib.parse import urlencode
from urllib.request import Request, urlopen

import sys
import time
import os
import json
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('myapp')
lastPush = datetime(2020,1,1)

loghandler = logging.handlers.TimedRotatingFileHandler("logfileGaurav",when="midnight")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
loghandler.setFormatter(formatter)
logger.addHandler(loghandler)
logger.setLevel(logging.DEBUG)

def getWFSlot(productUrl):
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
   }


   options = webdriver.ChromeOptions()
   #options.add_argument('headless')

   options.add_argument('--user-data-dir=chromeGaurav')
   #options.add_argument("profile-directory=chromeGaurav")

   driver = webdriver.Chrome(chrome_options=options)
   cookies = driver.get_cookies()
   #time.sleep(10)

   driver.get(productUrl)
   time.sleep(10)
   no_open_slots = True

   stores = {}
   stores['bjs'] = '26'
   stores['shoprite']='205'

   while no_open_slots:
      try:
         storesToPush = dict()
         for key in stores:
            driver.get('https://www.instacart.com/v3/retailers/' + stores[key]  +'/availability')
            driver.refresh()

            pre = driver.find_element_by_tag_name("pre").text

            # if key == 'bjs':
            #     pre = '{"retailer_availability": {"26": {"id": "133950192", "window": "Apr 26 - Apr 28", "services": ["delivery"], "availability": "Sun  800 AM - 1101 AM", "tracking_params": {"delivery_options": [{"id": 133950192, "available_ind": "True"}]}, "retailer_availability_text": "None"}}}'
            #     pre = '{"retailer_availability": {"26": null}}'
            # else:
            #   pre = '{"retailer_availability": {"205": {"id": "133950192", "window": "Apr 28 - Apr 29", "services": ["delivery"], "availability": "Sun  800 AM - 1101 AM", "tracking_params": {"delivery_options": [{"id": 133950192, "available_ind": "True"}]}, "retailer_availability_text": "None"}}}'
            #   pre = '{"retailer_availability": {"205": null}}'
            data = json.loads(pre)

            avail = data['retailer_availability']
            if avail[stores[key]]==None:
               logger.info('no dice :(')
            else:
               logger.info('check it out!')
               logger.info(data)
               wind=avail[stores[key]]['window'] + ',' + avail[stores[key]]['availability']

               if wind != 'See delivery times,See delivery times':
                  logger.info('window for pusher' + str(wind))
                  storesToPush[key] = wind
         if storesToPush.__len__() > 0:
              pusher(storesToPush)


      except:
         e = sys.exc_info()[0]
         logger.info(e)
         pass


      time.sleep(60)


def pusher(storesToPush):
   global lastPush
   logger.info("been asked to send notifications for " + ','.join(storesToPush.keys()))

   currPush = datetime.now()
   timediff = (currPush - lastPush).seconds
   logger.info("current timediff: " + str(timediff))

   if timediff < 300:
      logger.info("not pushing to ios now")

   else:
      logger.info("pushing to ios now")
      lastPush = currPush
      pushToMobile(storesToPush)


def pushToMobile(storesToPush):
   url = 'https://api.pushover.net/1/messages.json'  # Set destination URL here


   post_fields1 = {  # Set POST fields here
      "title": "Syosset Instacart Delivery Available for " + ','.join(storesToPush.keys()),
      "message": storesToPush,
      "token": "abshhmjf9u7vg9vynkjsuajyn28o3w",
      "user": "upjanbg18ykxb1gxk4hb9o8pdefpwv"
   }

   request1 = Request(url, urlencode(post_fields1).encode())
   json = urlopen(request1).read().decode()
   print(json)

   # post_fields2 = {  # Set POST fields here
   #    "title": "!!!!! Instacart Delivery Available for ",
   #    "message": store,
   #    "token": "abshhmjf9u7vg9vynkjsuajyn28o3w",
   #    "user": "upeg2h8xbzjp4gcfvn18aebtb3bamu"
   # }
   #
   # request2 = Request(url, urlencode(post_fields2).encode())
   # json2 = urlopen(request2).read().decode()
   # print(json2)
   #
   # post_fields3 = {  # Set POST fields here
   #    "title": "!!!!! Instacart Delivery Available for ",
   #    "message": store,
   #    "token": "abshhmjf9u7vg9vynkjsuajyn28o3w",
   #    "user": "uz5q7uxi84esaftmaers154irwg7o1"
   # }
   #
   # request3 = Request(url, urlencode(post_fields3).encode())
   # json3 = urlopen(request3).read().decode()
   # print(json3)


#getWFSlot('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')
getWFSlot('https://www.instacart.com')
#getWFSlot('https://www.instacart.com/v3/retailers/26/availability')

#{'retailer_availability': {'26': {'id': '133950192', 'window': 'Apr 26 - Apr 28', 'services': ['delivery'], 'availability': 'Sun,  8:00 AM - 11:01 AM', 'tracking_params': {'delivery_options': [{'id': 133950192, 'available_ind': True}]}, 'retailer_availability_text': None}}}
#"retailer_availability":{"26":null}}