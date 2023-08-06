from zjwbox.encrypt.login_all import LoginAll
import re


lg = LoginAll()
register_dict = {
    "lagou": lg.lagou,
    "douban": lg.douban,
    "taobao": lg.taobao,
    "zhihu": lg.zhihu,
    "jingdong": lg.jingdong,
    "baidupan": lg.baidupan,
    "QQZone": lg.QQZone,
    "ifeng": lg.ifeng,
    "eSurfing": lg.eSurfing,
    "zgconline": lg.zgconline,
    "github": lg.github,
    "zt12306": lg.zt12306,
    "music163": lg.music163,
    "sohu": lg.sohu,
    "bilibili": lg.bilibili,
    "weibo": lg.weibo,
    "youdao": lg.youdao,
    "renren": lg.renren
}


def GetSession(url):
    pattern = r"[http, https]://\w+.(.*?).com"
    domain = re.findall(string=url, pattern=pattern)[0]
    session = register_dict[domain]
    return session