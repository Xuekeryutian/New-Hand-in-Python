import requests




headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
'Chrome/63.0.3239.132 Safari/537.36'}
formdata = {
    'placeholder':'18875139211'
}
html = requests.post('https://www.zhihu.com',data=formdata,headers = headers)
html.encoding = html.apparent_encoding
print(html.text)