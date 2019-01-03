import re
import requests

url = "http://www.4399.com/"
html = requests.get(url)
html.encoding = html.apparent_encoding
#print(html.text)
#pattern = re.compile(".*(http://.*jpg).*")
#a=re.findall(pattern,str(html.text))
#print(a)
pattern = re.compile(".*?(\d+,'.*').*?")
a=re.findall(pattern,str(html.text))
print(a)






cangku = []
    for each_url in result:
        each_html = requests.get(each_url, headers=headers)
        each_html.encoding = each_html.apparent_encoding
        each_html = each_html.text
        par = re.compile("<.*>(.*)<.*>")
        result1 = re.findall(par, each_html)
        cangku.append(result1)
    return cangku