# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs

#set proxy variables as required
http_proxy  = "http://proxy.iiit.ac.in:8080"
proxyDict = { 
            "http": http_proxy,
            "https": http_proxy
            }

url = "http://www.redcafe.net/search/member?user_id=19580"
r = requests.get(url, proxies=proxyDict)
page_soup = bs(r.text, "lxml")
f = open('posts','w+')
f.write(page_soup.prettify().encode('utf-8'))
members = page_soup.findAll('div', attrs={"class":"titleText"})
for member in members:
    header_text = member.findAll('h3')
    for header in header_text:
        post_id = header.findAll('a')
    for post in post_id:
        post_text = str(post['href'])
        post_num = post_text[6:-1]
    print "\n"
# for member in members:
#     username = member.find('a', attrs = {'class' : 'username'})
#     print username
#     print "\n~~~~"