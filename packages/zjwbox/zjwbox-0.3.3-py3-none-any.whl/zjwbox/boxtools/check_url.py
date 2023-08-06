import re


def CheckUrl(url: str) -> all:
    register_domain = [
    "lagou",
    "douban",
    "taobao",
    "zhihu",
    "jingdong",
    "baidupan",
    "QQZone",
    "ifeng",
    "eSurfing",
    "zgconline",
    "github",
    "zt12306",
    "music163",
    "sohu",
    "bilibili",
    "weibo",
    "youdao",
    "renren"
    ]
    pattern = r"[http, https]://\w+.(.*?).com"
    result = re.findall(string=url, pattern=pattern)
    if result[0] in register_domain:
        return True
    else:
        return False

