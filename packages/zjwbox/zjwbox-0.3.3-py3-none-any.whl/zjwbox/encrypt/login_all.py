from DecryptLogin import login
from selenium import webdriver


lg = login.Login()



class LoginAll(object):
    def __init__(self):
        ...

    # 拉钩
    def lagou(self, username: str, password: str) -> all:
        return_info, session = lg.lagou(username, password, "pc")
        return session

    # 人人网
    def renren(self, username: str, password: str) -> all:
        return_info, session = lg.renren(username, password, "pc")
        return session

    # 豆瓣
    def douban(self, username: str, password: str) -> all:
        return_info, session = lg.douban(username, password)
        return session

    # 知乎
    def zhihu(self, username: str, password: str) -> all:
        return_info, session = lg.zhihu(username, password)
        return session

    # 有道
    def youdao(self, username: str, password: str) -> all:
        return_info, session = lg.youdao(username, password, "pc")
        return session

    # 微博
    def weibo(self, username: str, password: str) -> all:
        return_info, session = lg.weibo(username, password, "pc")
        return session

    # 哔哩哔哩
    def bilibili(self, username: str, password: str) -> all:
        return_info, session = lg.bilibili(username, password, "pc")
        return session

    # 搜狐
    def sohu(self, username: str, password: str) -> all:
        return_info, session = lg.sohu(username, password)
        return session

    # 网易云
    def music163(self, username: str, password: str) -> all:
        return_info, session = lg.music163(username, password)
        return session

    # 中国铁路12306
    def zt12306(self, username: str, password: str) -> all:
        return_info, session = lg.zt12306(username, password)
        return session

    # github
    def github(self, username: str, password: str) -> all:
        return_info, session = lg.github(username, password)
        return session

    # 中国在线中关村
    def zgconline(self, username: str, password: str) -> all:
        return_info, session = lg.zgconline(username, password)
        return session

    # 天翼
    def eSurfing(self, username: str, password: str) -> all:
        return_info, session = lg.eSurfing(username, password)
        return session

    # 凤凰网
    def ifeng(self, username: str, password: str) -> all:
        return_info, session = lg.ifeng(username, password)
        return session

    # QQ空间
    def QQZone(self, username: str, password: str) -> all:
        return_info, session = lg.QQZone(username, password)
        return session

    # 百度网盘
    def baidupan(self, username: str, password: str) -> all:
        return_info, session = lg.baidupan(username, password)
        return session

    # 淘宝
    def taobao(self, username: str, password: str) -> all:
        return_info, session = lg.taobao(username, password)
        return session

    # 京东
    def jingdong(self, username: str, password: str) -> all:
        return_info, session = lg.jingdong(username, password)
        return session


if __name__ == "__main__":
    e = LoginAll()
    session = e.jingdong("17685287506", "218347800wei")
    print(session)
    url = "https://www.renren.com"
    # res = session.get(url)
    # text = res.text
    # print(text)

    # print(cookie)
    # url = "https://www.douban.com"
    # driver = webdriver.Chrome("D:\\chromedriver\\chromedriver.exe")
    # driver.add_cookie(cookie)
    # driver.get(url)
    # driver.implicitly_wait(3)
    # input()