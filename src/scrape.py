#!/usr/bin/env python3

import requests 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import time
import random

list_papers=["Ettelaat","JomhouriEslami","KayhanNews"]
list_urls=[]

#creates list of urls for every issue of a paper 
for paper in list_papers:
  for i in range(1,14):
    url=f"https://www.pishkhan.com/pdfviewer.php?paper={paper}&date=1401{str(2).zfill(2)}{str(i).zfill(2)}"
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
