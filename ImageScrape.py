'''
Created on Aug 28, 2016
Description: run on Python 3.5. Not for Python 2.x

@author: AX
'''
from bs4 import BeautifulSoup
import requests
import re
import urllib.request as urllib2
import os
import http.cookiejar as cookielib
import json

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),"html.parser")

query = input("query image")# you can change the query for the image  here
# query='chinese food'
image_type = input("Image type")# you can change the query for the image  here
# image_type="Chinese_food"
query= query.split()
query='+'.join(query)
url="https://www.google.com/search?q="+query+"&source=lnms&tbm=isch"
print(url)

#add the directory for your image here
"""
# TODO: Consider defining a platform independent DIR.
delimiter = ('/', '//')[os.name == "nt"]
DIR = delimiter.join([os.path.expanduser('~'), "Downloads", "image_dw",
    (query.split('+'))[0], ""])
"""

DIR="//Users//Downloads//image_dw"+(query.split('+'))[0]+"//"
print(DIR)
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
soup = get_soup(url,header)


ActualImages=[]# contains the link for Large original images, type of image
for a in soup.find_all("div",{"class":"rg_meta"}):
    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
    ActualImages.append((link,Type))

print("there are total" , len(ActualImages),"images")
# ActualImages= ActualImages[0:1]
for i , (img , Type) in enumerate( ActualImages):
    try:
        print("img", img)
        req = urllib2.Request(img, headers=header)
        response = urllib2.urlopen(req)
        raw_img = response.read()
        if not os.path.exists(DIR):
            os.mkdir(DIR)
        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
        print ("imgNumber:", cntr)
        Type = (Type, "jpg")[len(Type) == 0]

        filepath = DIR + image_type + "_" + str(cntr) + "." + Type
        print("Saving to filepath: ", filepath)
        f = open(filepath, 'wb')
        f.write(raw_img)
        f.close()
    except Exception as e:
        print ("could not load : "+img)
        print (e)
