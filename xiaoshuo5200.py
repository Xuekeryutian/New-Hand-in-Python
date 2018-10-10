#coding:utf-8

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
'Chrome/63.0.3239.132 Safari/537.36'}
url = 'http://www.xiaoshuo520.com/book/tc4_ch0_d0_u0_ln0_e0_s0_f0_op0_p'
url_list = []
result = []
num = 1
for i in range(6):
    url_list.append(url+str(i)+'.html')
for j in url_list:
    res = requests.get(j).content.decode('utf-8')
    bs = BeautifulSoup(res,'html.parser')
    #print(bs)
    response = bs.findAll('span',{'class':'text'})

    for z in response:
        result.append(z.text)
        patterns = ['客服', '分享', '追书', '评论', '捧场', '目录']
    for k in patterns:
        result.remove(k)
result.sort()
for i in result:
    print(str(num)+"  "+i)
    num += 1






