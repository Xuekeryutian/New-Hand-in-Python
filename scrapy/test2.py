'''d = {"1":"2","3":"4","5":"6","7":"8"}
print(d["7"],d.get("7","9"))

try:
    n = 0
    n = input("a:")
    def pow10(n):
        return n ** 10
except:
    print("error")

a = ((3 ** 4 + (5*(6**7)))/8) ** 0.5
print("{:.3f}".format(a))
import jieba
s = "就在美国作为世界霸主"
print(len(s))
s1_list = jieba.lcut(s)
print(s1_list)port re
s = open("3.txt","r")
list = s.readlines()
#print(list)
for i in list:
    s = re.compile(".*\d\d\d\d\d{.html}")
    a = []
    b = re.findall(s,i)
    a.append(b)
print(a)'''
# import requests
# import readability
# from lxml import etree
# import time
# from selenium import webdriver
#
# def get_book(url = 'http://www.wqgzs.cn/'):
#
#     xpath = '/html/body/div/div[3]/div/div[2]/span[1]/text()'
#     html = requests.get(url)
#     html = html.text
#     html = etree.HTML(html)
#     a = html.xpath(xpath)
#     # a=readability.Document(html).summary()
#     print(a)
#
# def loap():
#     get_book()
#     time.sleep(10)
#     loap()
#
#
# if __name__ == '__main__':
#     loap()
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import json
#
# df = pd.DataFrame(pd.read_excel('name.xlsx'))
#
# df = pd.DataFrame({"id":[1001,1002,1003,1004,1005,1006],
#  "date":pd.date_range('20130102', periods=6),
#   "city":['Beijing ', 'SH', ' guangzhou ', 'Shenzhen', 'shanghai', 'Beijing '],
#  "age":[23,44,54,32,34,32],
#  "category":['100-A','100-B','110-A','110-C','210-A','130-F'],
#   "price":[1200,np.nan,2133,5433,np.nan,4432]},
#   columns =['id','date','city','category','age','price'])
# df1=pd.DataFrame({"id":[1001,1002,1003,1004,1005,1006,1007,1008],
# "gender":['male','female','male','female','male','female','male','female'],
# "pay":['Y','N','Y','Y','N','Y','N','Y',],
# "m-point":[10,12,20,40,40,40,30,20]})
#
# a = pd.merge(df,df1)
# print(a)
#
# a=a.set_index('id')
# print(a)
#
# df.loc[(df['city']=='Beijing')&(df['price']>=3000),'sign']=1
# print(df)
#
# a.to_excel('excel_to_thon.xlsx', sheet_name='bluewhale_cc')



if __name__ =='__main__':
    import requests
    import readability
    import re
    url = ('https://blog.csdn.net/liufang0001/article/details/77856255/')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             'Chrome/63.0.3239.132 Safari/537.36'}
    html = requests.get(url, headers=headers)
    readability.Document(html)
    html = html.text
    pattern = re.compile('<p>.*?</p>')
    a=re.findall(pattern,html)
    pattern1 = re.compile('<pre><code>(.*\s)</code></pre>')
    b = re.findall(pattern1, html)
    # str_ = ''
    # flag = 1
    # for ele in b:
    #     if ele == '<':
    #         flag = 0
    #     elif ele == '>':
    #         flag = 1
    #         continue
    #     if flag == 1:          delete html sysmbol
    #         str_ += ele



    print(b)
