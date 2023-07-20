#!/usr/bin/env python3

from argparse import FileType
import os
import subprocess
from asyncore import loop
import numpy as np
import argparse
import imutils
import cv2
import shutil
from difflib import SequenceMatcher
import re

issue="14000506"
month="05_1400"

os.chdir(f"/Users/andrewakhlaghi/Desktop/1year/etelaat/{month}/{issue}/")

for file in os.listdir():
  print(file)
  name=file[9:-4]
  subprocess.call(["convert", "-density", "300", file, name+".jpg"])

def sort_contours(cnts, method="left-to-right"):
  #initialize the reverse flag and sort index
  reverse = False
  i = 0
  #handle if we need to sort in reverse
  if method == "right-to-left" or method == "bottom-to-top":
    reverse = True
    #handle if we are sorting against the y-coordinate rather than
    #the x-coordinate of the bounding box
  if method == "top-to-bottom" or method == "bottom-to-top":
    i = 1
    #construct the list of bounding boxes and sort them from top to
    #bottom
  boundingBoxes = [cv2.boundingRect(c) for c in cnts]
  (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),key=lambda b:b[1][i], reverse=reverse))
  #return the list of sorted contours and bounding boxes
  return (cnts, boundingBoxes)

for file in os.listdir():
  if file.endswith(".jpg"):
    try:
      print(file)
      img = cv2.imread(file, 0)
      (thresh, img_bin) = cv2.threshold(img, 128, 255,cv2.THRESH_OTSU)
      img_bin = 255-img_bin
      #write gray scale image; cv2.imwrite("Image_bin.jpg",img_bin)
      #define kernels for detecting horizontal and vertical lines 
      kernel_length = np.array(img).shape[1]//80
      verticle_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, kernel_length))
      hori_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_length, 1))
      kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
      img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
      verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
      #write verticale lines ; cv2.imwrite("verticle_lines.jpg",verticle_lines_img)
      img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
      horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
      #write horizontal lines; cv2.imwrite("horizontal_lines.jpg",horizontal_lines_img)
      alpha=0.5
      beta=1.0-alpha
      img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
      img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
      (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128,255,cv2.THRESH_OTSU)
      #cv2.imwrite("img_final_bin.jpg",img_final_bin)
      #detect contrours and make bounding boxes 
      contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
      idx=0
      #uses location and dimensions of a contour/box to crop the advertisments and returns that image 
      for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        new_img = img[y:y+h, x:x+w]
        new_name=file[:-4]
        cv2.imwrite(new_name+"_"+str(idx) + ".jpg", new_img)
        idx += 1
    except:
      print("error", file)

#remove files that are too big/small on the assumption they are noise
for file in os.listdir():
  if file.endswith(".jpg") and os.path.getsize(file)>=4000000:
    os.remove(file)
  elif file.endswith(".jpg") and os.path.getsize(file)<100001:
    os.remove(file)
  else:
    pass

#convert jpg to tiffs, with appropriate density and noise removal, better ocr results
for file in os.listdir():
  if file.endswith(".jpg"):
    name=file[:-4]+".tiff"
    subprocess.call(["magick",file,"-despeckle","-despeckle","-despeckle","-despeckle","-despeckle","-despeckle","-despeckle","-despeckle","-despeckle","-despeckle","-despeckle","-despeckle","-despeckle","-despeckle","-despeckle","-despeckle","-despeckle","-despeckle","-despeckle","-despeckle","-despeckle",file])
    subprocess.call(["magick","-density","300",file,"-depth","8","-strip","-background","white","-alpha","off",name])

#ocr using tesseract, detects Persian only
for file in os.listdir():
  if file.endswith(".tiff"):
    name=file[:-5]
    subprocess.call(["tesseract", file, name,"-l","fas"])

#remove advertisements that don't contain at least one key word
for file in os.listdir():
  if file.endswith(".txt"):
    f=open(file,"r")
    filetext=f.read()
    if re.search("آگهی",str(filetext)):
      print(file, "True")
    elif re.search("فراخوان",str(filetext)):
      print(file, "True")
    elif re.search("شناسه ملی",str(filetext)):
      print(file, "True")
    elif re.search("شماره ملی",str(filetext)):
      print(file, "True")
    elif re.search("شناسه",str(filetext)):
      print(file, "True")
    elif re.search("سهامی خاص",str(filetext)):
      print(file, "True")
    else:
      name_base=file[:-4]
      print(name_base)
      os.remove(file)
      os.remove(name_base+".jpg")
      os.remove(name_base+".tiff")

l1=os.listdir()
l1_text=[]
for file in l1:
  if file.endswith(".txt"):
    l1_text.append(file)
  
l2_text=l1_text

#remove overly similar advertisements, may have detect the same one multiple times due to complicated borders
to_be_removed=[]
for file_1 in l1_text:
  for file_2 in l2_text:
    file1_open=open(file_1).read()
    file2_open=open(file_2).read()
    m = SequenceMatcher(None, file1_open, file2_open)
    if m.ratio()>0.4 and m.ratio()<1:
      print(file_1, file_2, m.ratio())
      to_be_removed.append(file_2)
      print(file_1)
      try:
        l2_text.remove(file_1)
      except:
        pass

set_to_be_removed=set(to_be_removed)
for file in set_to_be_removed:
  try:
    base_file=file[:-4]
    os.remove(file)
    os.remove(base_file+".tiff")
    os.remove(base_file+".jpg")
  except:
    print(file)

os.mkdir("articles_pic")
os.mkdir("articles_text")

for file in os.listdir():
  if file.endswith(".jpg"):
    os.rename(file,f"/Users/andrewakhlaghi/Desktop/1year/etelaat/{month}/{issue}/articles_pic/"+file)
  elif file.endswith(".tiff"):
    os.remove(file)
  elif file.endswith(".txt"):
    os.rename(file,f"/Users/andrewakhlaghi/Desktop/1year/etelaat/{month}/{issue}/articles_text/"+file)
  else:
    pass
