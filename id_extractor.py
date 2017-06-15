# -*- coding: utf-8 -*-
# import sys
import requests
from bs4 import BeautifulSoup as bs

#set proxy variables as required
http_proxy  = "http://proxy.iiit.ac.in:8080"
proxyDict = { 
            "http": http_proxy,
            "https": http_proxy
            }
dict_entry = {'Member_Id':'Name'}
url = "http://www.redcafe.net/online/?type=registered"
r = requests.get(url, proxies=proxyDict)
page_soup = bs(r.text, "lxml")
members = page_soup.findAll(attrs={"class":"memberListItem"})
for member in members:
    username = member.find('a', attrs = {'class' : 'username'})
    id_string = username['href']
    member_id = id_string[(id_string.index('.')+1):-1]
    # print member_id
    for name in username:
        # print name
        dict_entry[member_id] = name

f = open('output','a+')
for key, item in dict_entry.iteritems():
    dict_text = key+"\t"+item+"\n"
    f.write(dict_text.encode('utf-8'))
