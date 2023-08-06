import requests
import parsel, re, json, jsonpath
import time, random, sys, psutil
import asyncio, aiohttp
from tqdm import tqdm
from itertools import product
import eventlet
from faker import Faker
from datetime import datetime
from zjwbox.boxtools.time_delay import DelayWait
from zjwbox.boxtools.log_set import LogSet
from zjwbox.boxtools.proxyShop import get_proxy
from zjwbox.boxtools.check_url import CheckUrl
from zjwbox.boxtools.get_session import GetSession
import os
# os.environ['NO_PROXY'] = 'stackoverflow.com'

"""
This is a person to solve common spider in website.
You may transmit some args to it.
Least need a arg(url or urls), 
of couser, you also can change many args, headers cookie, data, mode, etc.
Matters need attention: urls should be a string or list. 
"""

# data of faker
fake = Faker()
# product of user-agent
fake_ua = fake.user_agent()


class Comm_req(object):

    def __init__(self, urls: str or list, headers: dict={"UserAgent": fake_ua}, cookie: dict=None, data: dict=None, 
                        encode: str="utf-8", mode: str="get", time_inter: bool=True, debug_mode: str="no", is_proxy=False):
        self.urls = urls
        self.headers = headers
        self.cookie = cookie
        self.data = data
        self.mode = mode
        self.encode = encode
        self.time_inter = time_inter
        self.is_proxy = is_proxy
        # log
        self.logger = LogSet().debug_log(levelname=debug_mode)
        self.log = LogSet().output_log(levelname="debug")
        self.debug = self.logger.warning
        self.warn = self.logger.info
        self.error = self.logger.debug
        self.record = self.log.info


    async def fask(self, url, mode="get") -> str:
        async with aiohttp.ClientSession() as session:
            if self.mode == "post":
                async with session.post(url, headers=self.headers, data=self.data, timeout=3) as res:
                    return await res.text()
            else:
                async with session.get(url, headers=self.headers, timeout=3) as res:
                    return await res.text()

    def get_proxys(self) -> dict:
        get_proxy()
        with open("getProxy.txt", mode="r", encoding="utf-8", errors='ignore') as f:
            # ip = f.read()
            return json.load(f, strict=False)


    def comm_deal(self, expr_element: list or tuple or str, is_json: bool=False, session=requests.Session()) -> str:
        if isinstance(self.urls, str):
            if self.time_inter:
                res = session.get(self.urls, headers=self.headers, timeout=5)
                text = res.content.decode(self.encode)
                if self.is_proxy and self.mode == "get":
                    proxies = self.get_proxys()
                    try:
                        res = session.get(self.urls, headers=self.headers, timeout=5, proxies=proxies)
                        text = res.content.decode(self.encode)
                    except requests.exceptions.ReadTimeout as e:
                        print("ip失效！")
                        return None
                if self.mode == "post":
                    res = session.post(self.urls, headers=self.headers, data=self.data)
                    text = res.content.decode(self.encode)
                    if self.is_proxy:
                        proxies = self.get_proxys()
                        try:
                            res = session.post(self.urls, headers=self.headers, data=self.data, proxies=proxies)
                            text = res.content.decode(self.encode)
                        except requests.exceptions.ReadTimeout as e:
                            print("ip失效！")
                            return None
                delay = DelayWait()
                delay.wait(self.urls)
                if is_json:
                    json_text = jsonpath.jsonpath(json.loads(text), f"$..{expr_element}")
                    self.debug("json_text：" + str(json_text))
                    self.record(json_text)
                    yield json_text
                else:
                    self.debug("text：" + str(text) )
                    self.record(text)
                    yield text

            else:
                try:
                    proxies = self.get_proxys()
                    res = session.get(self.urls, headers=self.headers, proxies=proxies, timeout=5)
                    self.debug("res：" + str(res))
                    self.record(res)
                    text = res.content.decode(self.encode)
                    self.debug("text：" + str(text))
                    self.record(text)
                except requests.exceptions.ReadTimeout as e:
                    print("ip失效！")
                    return None
                if self.is_proxy and self.mode == "get":
                    try:
                        proxies = self.get_proxys()
                        res = session.get(self.urls, headers=self.headers, timeout=5, proxies=proxies)
                    except requests.exceptions.ReadTimeout as e:
                        print("ip失效！")
                        return None       
                    else:             
                        self.debug("res：" + str(res))
                        self.record(res)
                        text = res.content.decode(self.encode)
                        self.debug("text：" + str(text))
                        self.record(text)
                if self.mode == "post":
                    res = session.post(self.urls, headers=self.headers, data=self.data)
                    self.debug("res：" + str(res))
                    self.record(res)
                    text = res.content.decode(self.encode)
                    self.debug("text：" + str(text))
                    self.record(text)
                    if self.is_proxy:
                        proxies = self.get_proxys()
                        try:
                            res = session.post(self.urls, headers=self.headers, data=self.data, proxies=proxies)
                            self.debug("res：" + str(res))
                            self.record(res)
                            text = res.content.decode(self.encode)
                            self.debug("text：" + str(text))
                            self.record(text)
                        except requests.exceptions.ReadTimeout as e:
                            print("ip失效！")
                            return None                            
                yield text

        else:
            for url in self.urls:
                loop = asyncio.get_event_loop()
                text = loop.run_until_complete( self.fask(url, self.mode) )
                self.debug("text：" + str(text))
                self.record(text)
                now_time = datetime.now()
                print(f"爬取{url}成功！时间：{now_time}")
                delay = DelayWait()
                delay.wait(url)
                yield text


    def get_page(self, expr_element: list or tuple or str="", is_json: bool=False, login_args: dict=None):
        result = []
        if CheckUrl(self.urls):
            session = GetSession(self.urls)(login_args["username"], login_args["password"])
            for page in self.comm_deal(expr_element, is_json=is_json, session=session):
                result.append(page)

        for page in self.comm_deal(expr_element, is_json=is_json):
            result.append(page)
        if result == []:
            return None
        eventlet.monkey_patch()
        now_time = datetime.now()
        if isinstance(self.urls, str):
            print(f"目标1个，成功爬取{len(result)}, 时间：{now_time}")
        else:
            print(f"目标{len(self.urls)}个，成功爬取{len(result)}，时间：{now_time}")
  
        return result
        




if __name__ == "__main__":
    url = "http://hgk.guizhou.gov.cn/gzdata/getGroupTableData.action"
    data = {
        "tableId": 725,
        "year_limit": 1,
        "address_code": "0001",
        "field_code": "0002"
    }
