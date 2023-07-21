#!/usr/bin/env python3

import requests 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import time
import random

import requests 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import time
import random

list_papers=["Ettelaat","JomhouriEslami","KayhanNews"]
list_urls=[]

#collects dates of publication one month at a time
r=requests.get(f"https://www.pishkhan.com/rooznameh/Ettelaat?date=140004")
print(r)
list_dates=re.findall("140004(\d+)",str(r.text))
set_dates=set(list_dates)

#check for debugging
print(set_dates)

#creates urls for all issues of a newspaper in a month
for paper in list_papers_:
  for i in set_dates: 
    url=f"https://www.pishkhan.com/pdfviewer.php?paper={paper}&date=1400{str(4).zfill(2)}{str(i).zfill(2)}"
    list_urls.append(url)

#wait times are meant to prevent cloudflare IP blocking
for url in list_urls:
  wait_time=random.randint(20,30)
  print(wait_time)
  browser = webdriver.Safari()
  browser.get(url)
  time.sleep(wait_time)
  url_pdf=browser.current_url
  date=url.split("date=")[1]
  paper=re.search("\?paper=(\w+)&",url)[1]
  flname=f"{paper}_{date}"+".pdf"
  print(flname)
  with open(flname, "wb") as f:
    r=requests.get(url_pdf)
    f.write(r.content)
  f.close()
  browser.close()
  time.sleep(wait_time)
