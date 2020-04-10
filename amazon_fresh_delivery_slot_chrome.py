import bs4
from selenium import webdriver

from datetime import datetime,timedelta

import sys
import time
import os


def getWFSlot(productUrl):
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
   }


   options = webdriver.ChromeOptions()
   options.add_argument("user-data-dir=selenium")

   driver = webdriver.Chrome(chrome_options=options)

   #cook = driver.get_cookies();
   driver.get(productUrl)
   html = driver.page_source
   soup = bs4.BeautifulSoup(html,"html.parser")
   time.sleep(60)
   no_open_slots = True

   t1 = 'No doorstep delivery windows are available for Today, Apr 9.'
   t2 = 'No doorstep delivery windows are available for Friday, Apr 10.'
   t3 = 'No doorstep delivery windows are available for Saturday, Apr 11.'
   t4 = 'No doorstep delivery windows are available for Sunday, Apr 12.'
   t5 = 'No doorstep delivery windows are available for Monday, Apr 13.'


   while no_open_slots:
      driver.refresh()

      t1date = datetime.today()
      t1 = 'No doorstep delivery windows are available for Today'
      t2 = 'No doorstep delivery windows are available for ' + str((t1date + timedelta(days=1)).strftime('%A'))
      t3 = 'No doorstep delivery windows are available for ' + str((t1date + timedelta(days=2)).strftime('%A'))
      t4 = 'No doorstep delivery windows are available for ' + str((t1date + timedelta(days=3)).strftime('%A'))

      print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), " refreshed!!!!")
      html = driver.page_source
      soup = bs4.BeautifulSoup(html,"html.parser")

      slot_patterns = ['Next available', '1-hour delivery windows', '2-hour delivery windows']

      t1pos = soup.text.find(t1)
      if t1pos < 0:
         print('SLOTS OPEN TODAY!')
         os.system('say "Slots for delivery opened today!"')

      t2pos = soup.text.find(t2)
      if t2pos < 0:
         print('SLOTS OPEN!! ', t2.split()[-1])
         os.system('say "Slots for delivery opened t2!"')

      t3pos = soup.text.find(t3)
      if t3pos < 0:
         print('SLOTS OPEN ! ', t3.split()[-1])
         os.system('say "Slots for delivery opened t3!"')

      t4pos = soup.text.find(t4)
      if t4pos < 0:
         print('SLOTS OPEN ! ', t4.split()[-1])
         os.system('say "Slots for delivery opened t4!"')


      try:
         no_slot_pattern = 'No delivery windows available. New windows are released throughout the day.'
         if no_slot_pattern == soup.find('h4', class_ ='a-alert-heading').text:
            print("NO SLOTS!")
      except AttributeError: 
            print('SLOTS OPEN!')
            os.system('say "Slots for delivery opened three!"')
            #no_open_slots = False
      time.sleep(30)

getWFSlot('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')
#getWFSlot('https://www.google.com')

