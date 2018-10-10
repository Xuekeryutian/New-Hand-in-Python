'''import urllib.request
import re

list_url=[]

url="https://movie.douban.com/top250?start="
num=1
for i in range(4):
    list_url.append(url+str(i*25))
for j in list_url:
    html=urllib.request.urlopen(j).read().decode('utf-8')
    top_tag=re.compile(r'<span class="title">(.*)</span>')
    title=re.findall(top_tag,html)

    for j in title:

        if j.find("/") == -1:
            print('top'+str(num)+'     '+j)
            num+=1
'''
import re
import requests
from bs4 import BeautifulSoup

top_num=1
url="https://movie.douban.com/top250?start="
urls=[url+str(num*25) for num in range(4)]
for url in urls:
    r=requests.get(url)
    html=r.text
    soup=BeautifulSoup(html, 'html.parser')
    movie=soup.find_all("span",class_="title")
    for i in movie:
        if i.text.find('/')==-1:
            print('top'+str(top_num)+'   '+i.text)
            top_num+=1
