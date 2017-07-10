import sys
import requests
from bs4 import BeautifulSoup as bs

#set proxy variables as required
http_proxy  = "http://proxy.iiit.ac.in:8080"
proxyDict = { 
            "http": http_proxy,
            "https": http_proxy
            }

# open the file specified
urls = open("./yearwise_urls/urls_list_2014.txt","r+").readlines()
article_count = float(len(urls))

for idx, url in enumerate(urls):
    url = url.strip()
    r = requests.get(url, proxies=proxyDict)
    article_soup = bs(r.text, "html.parser")

    percent = float(idx+1)/article_count*100.000000
    sys.stdout.write("\rExtracting Articles: %d/%d - %f%% done." % ((idx+1), article_count, percent))
    sys.stdout.flush()

    f = open('./yearwise_articles/articles_2014.txt', 'a+')

    #Article Delimiter
    delim = "\n\n~~~~#%s~~~~\n\n" % (idx+1)
    f.write(delim.encode('utf-8'))

    # Extracting Title of Article
    title_text = article_soup.find(attrs={"class":"content__headline"})
    if (title_text != None):
        title_list = list(set(title_text))
        for each in title_list:
            title = each.encode('utf-8').strip()
            title_write = "~~TITLE~~\n%s\n" % title
    else:
        title_write = "~~TITLE~~\nEmpty\n"
    f.write(title_write)

    #Extracting Author Name
    for tag in article_soup.find_all("meta"):
        if tag.get("name", None) == "author":
            author = tag.get("content", None)
            author_write = "~~AUTHOR~~\n%s\n" % author
            f.write(author_write.encode('utf-8'))

    # Extracting Article Contents
    text = ""
    result = article_soup.find(attrs={"class":"content__article-body"})
    if ( result != None ):
        text = result.get_text()
        f.write("~CONTENTS~\n")
    for para in text:
        if para != '\n':
            f.write(para.encode('utf-8'))

    #Extracting Article Topic Keywords
    topic_set = article_soup.find(attrs={"data-link-name":"article section"})
    if topic_set != None:
        topic_set = list(set(topic_set))
        for each in topic_set:
            topic = each.encode('utf-8').strip()
            topic_write = "\n~~TOPIC~~\n%s\n" % topic
    else:
        topic_write = "\n~~TOPIC~~\nEmpty\n"
    f.write(topic_write)

    # Extracting Article Publishing Time
    for match in article_soup.findAll('span'):
        match.unwrap()
    time_set = article_soup.find(attrs={"class":"content__dateline-wpd js-wpd"})
    if time_set != None:
        time = time_set.get_text().strip()
        time_write = "~~TIMESTAMP~~\n%s\n" % time
    else:
        time_write = "~~TIMERSTAMP~~\nEmpty\n"
    f.write(time_write.encode('utf-8'))

print("\nCompleted!")