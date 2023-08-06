# -*- coding: utf-8 -*-
from urllib import parse
from datetime import datetime
import time, random


rand_delay = random.uniform(0.9, 1.5)

class DelayWait(object):
    def __init__(self, delay=rand_delay):
        self.delay = delay
        self.urls = dict()
        # 重复次数
        self.count = 0

    def wait(self, url: str) -> None:
        netloc = parse.urlparse(url).netloc
        lastOne = self.urls.get(netloc)
        # 是否已请求过
        if lastOne and self.delay > 0:
            # 两次时间差
            timeWait = self.delay - (datetime.now() - lastOne).seconds
            if timeWait > 0:
                if self.count > 4 and self.count < 15:
                    time.sleep(timeWait * 2)
                    self.count += 1
                elif self.count > 15:
                    time.sleep(timeWait * 3)
                    self.count += 1
                else:
                    time.sleep(timeWait)
                    self.count += 1
        self.urls[netloc] = datetime.now()

