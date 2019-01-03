'''import pickle
import time
from selenium import webdriver



url = "http://www.jiaowu.shisu.edu.cn/eams/login.action"
web_driver = webdriver.Chrome()
web_driver.get(url)

username = web_driver.find_element_by_id('login-email')
username.send_keys('username')
password = web_driver.find_element_by_id('login-password')
password.send_keys('password')
login_button = web_driver.find_element_by_id('login-submit')
login_button.click()
time.sleep(3)
cookies = web_driver.get_cookies()
web_driver.close()
print(cookies)'''
import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
html = requests.get('http://www.qishu.cc/txt/12345.html')
html.encoding = 'gb2312'  # 防止中文乱码
html_deal = etree.HTML(html.text)
introduce = html_deal.xpath('//*[@id="mainSoftIntro"]/p[2]/text()')
name = html_deal.xpath('//*[@id="downAddress"]/a[2]/b/text()')
'''
      for i in introduce:
          for j in name:
              f.writelines(i+"   "+j+"\n")'''
print(str(name)+":  "+str(introduce))






