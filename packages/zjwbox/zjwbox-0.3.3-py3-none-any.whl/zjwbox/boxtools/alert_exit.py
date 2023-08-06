from atexit import register
from datetime import datetime
import sys, psutil, os


def alertExit() -> None:
    info = psutil.virtual_memory()
    print(u'内存使用：',psutil.Process(os.getpid()).memory_info().rss)
    print(u'总内存：',info.total)
    print(u'内存占比：',info.percent)
    print(u'cpu个数：',psutil.cpu_count())
    print("感谢使用！", datetime.now())
    print("-"*30)
#     dealExit()


# @register
# def dealExit() -> str:
#     sys.exit(0)


