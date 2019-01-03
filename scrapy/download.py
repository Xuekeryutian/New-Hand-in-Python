from Tgrottle import Throttle
import random


class Downloader:
    def __int__(self,delay = 5,
                proxies = None,
                num_retries = 1,
                cache = None):
        self.throttle = Throttle(delay)
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache


        def __call__(self,url):
            result = None
            if self.cache:
                try:
                    result = self.cache[url]
                except KeyError:
                    pass
                else:
                    if self.num_retries > 0 and \
                        500 <= result['code'] < 600:
                        result = None
            if result is None:
                self.throttle.wait(url)
                proxy = random.choice(self.proxies) if self.proxies else None
                headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
'Chrome/63.0.3239.132 Safari/537.36'}
                result = self.download(url,headers,proxy,self.num_retries)
                if self.cache:
                    self.cache[url] = result
            return result['html']