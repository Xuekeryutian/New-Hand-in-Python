from newspaper import Article

url ='https://www.cnblogs.com/themost/p/6900852.html'
article = Article(url, language='zh')
article.download()
article.parse()
print(article.text)
