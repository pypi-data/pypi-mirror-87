from pyquery import PyQuery as pq
import re
from requests.exceptions import ConnectionError
from fake_useragent import UserAgent, FakeUserAgentError
import requests
import random
import time, json
import threading, asyncio
import eventlet
from zjwbox.boxtools.log_set import LogSet


logger = LogSet().debug_log(levelname="debug")
log = LogSet().output_log(levelname="debug")
debug = logger.warning
warn = logger.info
error = logger.debug
record = log.info

def get_page(url, options={}):
    try:
        ua = UserAgent()
    except FakeUserAgentError:
        pass
    # 生成随机的请求头，加 try...except... 使代码更加健壮
    base_headers = {
        'User-Agent': ua.random,
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    # 如果使用者有传入请求头，则将此请求头和随机生成的合成在一起
    headers = dict(base_headers, **options)
    # 当前请求的 url
    print('Getting', url)
    try:
        r = requests.get(url, headers=headers)
        print('Getting result', url, r.status_code)
        if r.status_code == 200:
            return r.text
        return None
    except ConnectionError:
        print('Crawling Failed', url)
        return None


class ProxyMetaclass(type):

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(object, metaclass=ProxyMetaclass):
    """
    免费代理获取
    1. 快代理
    2. 西拉代理
    3. 66代理
    4. 无忧代理
    5. 开心代理-高匿
    """

    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback', callback)
        for proxy in eval("self.{}()".format(callback)):
            print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies

    def crawl_kuaidaili(self):
        """
        快代理
        :return:
        """
        for page in range(1, 4):
            start_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)
            html = get_page(start_url)
            pattern = re.compile(
                '<td data-title="IP">(.*)</td>\s*<td data-title="PORT">(\w+)</td>'
            )

            ip_addres = pattern.findall(str(html))
            for adress, port in ip_addres:
                # print(adress, port)
                result = f"{adress}:{port}".strip()
                yield result

    def crawl_xicidaili(self):
        """
        西拉代理
        :return:
        """
        for page in range(1, 4):
            start_url = 'http://www.xiladaili.com/'
            html = get_page(start_url)
            pattern = r"<>(\d+.\d+.\d+.\d+:\d+)<>"
            ip_adress = re.findall(string=html, pattern=pattern)
            for ip in ip_adress:
                result = ip.strip()
                yield result

    def crawl_daili66(self, page_count=4):
        """
        66代理
        :param page_count:
        :return:
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            record('Crawling' + url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_data5u(self):
        """
        无忧代理
        :return:
        """
        start_url = 'http://www.data5u.com'
        html = get_page(start_url)
        # print(html)
        ip_adress = re.compile(
            '<ul class="l2">\s*<span><li>(.*?)</li></span>\s*<span style="width: 100px;"><li class=".*">(.*?)</li></span>'
        )
        # \s * 匹配空格，起到换行作用
        re_ip_adress = ip_adress.findall(str(html))
        for adress, port in re_ip_adress:
            result = f"{adress}:{port}"
            yield result.strip()

    def crawl_kxdaili(self):
        """
        开心代理-高匿
        :return:
        """
        for i in range(1, 4):
            start_url = 'http://www.kxdaili.com/dailiip/1/{}.html'.format(i)
            try:
                html = requests.get(start_url)
                if html.status_code == 200:
                    html.encoding = 'utf-8'
                    # print(html.text)
                    ip_adress = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
                    # \s* 匹配空格，起到换行作用
                    re_ip_adress = ip_adress.findall(str(html.text))
                    for adress, port in re_ip_adress:
                        result = f"{adress}:{port}"
                        yield result.strip()
                return None
            except:
                pass


def kuaidaili():
    result = []
    proxy = FreeProxyGetter()
    kuaidailis = proxy.crawl_xicidaili()

    for kuaidaili in kuaidailis:
        result.append(kuaidaili)
    return result


def xicidaili():
    result = []
    proxy = FreeProxyGetter()
    xicidailis = proxy.crawl_xicidaili()

    for xicidaili in xicidailis:
        result.append(xicidaili)
    return result


def data5u():
    result = []
    proxy = FreeProxyGetter()
    data5us = proxy.crawl_data5u()

    for data5u in data5us:
        result.append(data5u)
    return result


def kxdaili():
    result = []
    proxy = FreeProxyGetter()
    kxdailis = proxy.crawl_kxdaili()

    for kxdaili in kxdailis:
        result.append(kxdaili)
    return result


def daili66():
    result = []
    proxy = FreeProxyGetter()
    daili66s = proxy.crawl_daili66()
    kxdailis = proxy.crawl_kxdaili()

    for daili66 in daili66s:
        result.append(daili66)
    for kxdaili in kxdailis:
        result.append(kxdaili)
    return result


class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result   # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

def allproxy():
    result = []
    proxy = FreeProxyGetter()

    daili66s = proxy.crawl_daili66()
    data5us = proxy.crawl_data5u()
    kxdailis = proxy.crawl_kxdaili()
    xicidailis = proxy.crawl_xicidaili()
    kuaidailis = proxy.crawl_kuaidaili()

    for kuaidaili in kuaidailis:
        result.append(kuaidaili)

    for xicidaili in xicidailis:
        result.append(xicidaili)

    for kxdaili in kxdailis:
        result.append(kxdaili)

    for data5u in data5us:
        result.append(data5u)

    for daili66 in daili66s:
        result.append(daili66)

    return result

# return of result
use_proxy = []


async def usefulProxy(i):
    try:

        ip_proxy = i  # random.choice(http_ip)
        proxy_ip = {
            'http': ip_proxy,
            'https': ip_proxy,
        }
        print('使用代理的IP:', proxy_ip)
        response = requests.get("http://httpbin.org/ip", proxies=proxy_ip, timeout=1).text
        print('\033[1;32m当前IP有效\033[0m')
        record('\033[1;32m当前IP有效\033[0m')
        use_proxy.append(proxy_ip)
        with open("getProxy.txt", mode="w", encoding="utf-8") as fg:
            fg.write( json.dumps(proxy_ip) )
        return
    except Exception as e:
        print(e.args[0])
        print('\033[1;31m当前IP无效\033[0m')
        record(e.args[0])
        record('\033[1;31m当前IP无效\033[0m')


async def get_task():
    all_proxy = allproxy()
    tasks = [asyncio.ensure_future(usefulProxy(i)) for i in all_proxy]
    await asyncio.gather(*tasks)


def get_proxy():
    # asyncio deal
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_task())

    eventlet.monkey_patch()
    while not use_proxy:
        print("没有可用的IP，准备重启中...")
        with eventlet.Timeout(5, False):
            for i in range(5,0,-1):
                print(f"\r正在重启，倒计时{i+1}秒...", flush=True, end="")
                time.sleep(1)
        get_proxy()

    return use_proxy



# a example of !
if __name__ == "__main__":
    a = get_proxy()
    print(a)
