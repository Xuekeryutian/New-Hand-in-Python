from random import *
import requests
from lxml import etree
i = randint(10000,99999)
f = open('url.txt','w+')
for j in range(50):
    f.writelines("http://www.qishu.cc/txt/"+str(randint(10000,99999))+".html"+"\n")
f1 = f.readlines()
for i in f1:
    html = requests.get('i')
    html.encoding = 'gb2312'  # 防止中文乱码
    html_deal = etree.HTML(html.text)
    introduce = html_deal.xpath('//*[@id="mainSoftIntro"]/p[2]/text()')
    name = html_deal.xpath('//*[@id="downAddress"]/a[2]/b/text()')
    f2 = open('3.txt','w+')
    f2.writelines(str(name)+":  "+str(introduce)+'\n')

