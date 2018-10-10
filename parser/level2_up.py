#coding:utf-8

import requests
from bs4 import BeautifulSoup
import re
from lxml import etree









headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
'Chrome/63.0.3239.132 Safari/537.36'}

#url = 'http://www.qishu.cc/xuanhuan/list1_'

def Get_url(url,loap_number):
    url_list = []
    for i in range(loap_number):
        url_list.append(url+str(i)+'.html')
    return url_list

#print(url_list)
def Get_deeper_url(list):
    url_list1 = []
    response_list = []
    patterns = re.compile(r'\d\d\d\d\d')

    for i in(list):
        html = requests.get('http://www.qishu.cc/xuanhuan/list1_1.html')
        html.encoding = html.apparent_encoding       #防止中文乱码
        soup = BeautifulSoup(html.text,'html.parser')
        response = soup.findAll('span',{'class':'mainSoftName'})
        number_list = re.findall(patterns,str(response))
    for i in number_list:
        url_list1.append("http://www.qishu.cc/txt/" + str(i) + ".html")
    return url_list1
def dowload(list):
    introduce = []
    name = []
    for each_url in list:
        html = requests.get(each_url)
        html.encoding = 'gb2312'           #防止中文乱码
        html_deal = etree.HTML(html.text)
        introduce.append(html_deal.xpath('//*[@id="mainSoftIntro"]/p[2]/text()'))
        name.append(html_deal.xpath('//*[@id="downAddress"]/a[2]/b/text()'))
    return introduce








if __name__ == '__main__':
    a = dowload(Get_deeper_url(Get_url('http://www.qishu.cc/xuanhuan/list1_',4)))
    with open("name","a") as f:
        for i in a:
            f.writelines(i+"\n")








