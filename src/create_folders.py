#!/usr/bin/env python3
import os
newspaper='jomhouri_eslami'
month='07_1400'
list_issues=[]
os.chdir(f'/Users/andrewakhlaghi/Desktop/1year/{newspaper}/{month}')

for issue in os.listdir():
    list_issues.append(issue)

for issue in list_issues:
    try:
        os.chdir(f"/Users/andrewakhlaghi/Desktop/1year/{newspaper}/{month}/{issue}")
        for file in os.listdir('articles_pic'):
            os.mkdir(file[:-4])
        for file in os.listdir('articles_pic'):
            dir=file[:-4]
            origin=f"/Users/andrewakhlaghi/Desktop/1year/{newspaper}/{month}/{issue}/articles_pic/{file}"
            os.rename(origin, f"/Users/andrewakhlaghi/Desktop/1year/{newspaper}/{month}/{issue}/{dir}/{file}")
        for file in os.listdir('articles_text'):
            dir=file[:-4]
            origin=f"/Users/andrewakhlaghi/Desktop/1year/{newspaper}/{month}/{issue}/articles_text/{file}"
            os.rename(origin, f"/Users/andrewakhlaghi/Desktop/1year/{newspaper}/{month}/{issue}/{dir}/{file}")
        os.rmdir("articles_pic")
        os.rmdir("articles_text")
    except:
        print(issue)
