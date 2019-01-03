import re
import requests
from itertools import *


def seach(seach_name):
    url = ("https://so.csdn.net/so/search/s.do?q=" + str(seach_name))
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
    'Chrome/63.0.3239.132 Safari/537.36'}
    html = requests.get(url, headers=headers)
    html.encoding = html.apparent_encoding
    pattern = re.compile(".*<a href=.(.*\d*)target")

    result = re.findall(pattern,str(html.text))
    result.sort()
    result = [k for k, g in groupby(result)]   #删除数组中重复的元素
    return result


























if __name__ == '__main__':
    seach_name = input("输入你要搜索的问题:    ")
    print(seach(seach_name))



