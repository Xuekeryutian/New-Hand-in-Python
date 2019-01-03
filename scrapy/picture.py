import requests
import time
import os
import re
import random

class Spider(object):
    def __init__(self):
        self.url = "http://sozaing.com/category/photo/365photo/page/{}/"
    @staticmethod
    def get_html(url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
    'Chrome/63.0.3239.132 Safari/537.36'}
        html = requests.get(url,headers = headers)
        html = html.text
        return html

    def get_onepage(self,url):
        html = self.get_html(url)
        pattern = re.compile('<p class="title"><a href="(.*?)">(.*?)</a></p>',re.S)
        result = re.findall(pattern,html)
        picture_list = []
        page = int(url.split('/')[7])
        num = 1
        self.mkdir(page)
        for i in result:
            html2 = self.get_html(i[0])
            picture_link = re.findall('<p class="mar_b_25 center".*?<img.*?src="(.*?)".*?</p>',html2,re.S)
            if picture_link:
                picture_list.append(picture_link)
                pic_path = 'C:\\用户\\t\\PycharmProjects\\scrapy\\%s\\%s.jpg'%(page,i[1])
                e = os.path.exists(pic_path)
                if not e:
                    pic = requests.get(picture_link[0])
                    with open(pic_path,'wb') as f:
                        f.write(pic.content)
                    print('第'+str(num)+'张')
                else:
                    print('have now')
                num += 1

    @staticmethod
    def mkdir(i):
        filename = str(i)
        path = ('C:\\用户\\t\PycharmProjects\\scrapy\\%s'%filename)
        os.makedirs(path)
    def getmore(self):
        html = self.get_html('http://sozaing.com/category/photo/365photo/page/1/')
        last_page = re.findall("<span class='pages'>Page 1of (\d+)</span>",html)
        for i in range(1,10):
            url = self.url.format(i)
            self.get_onepage(url)

if __name__ == "__main__":
    spider = Spider()
    spider.getmore()







