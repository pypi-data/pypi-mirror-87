import logging
import sys


class LogSet(object):
    def __init__(self, mod_name=None):
        self.mod_name = __name__

    def debug_log(self, levelname: str) -> all:
        levels = {
            "error": logging.DEBUG,
            "warn": logging.INFO,
            "debug": logging.WARNING,
            "no": logging.ERROR
        }
        logging.basicConfig(
            level=levels[levelname],
            format="\033[1;31m%(message)s\n%(asctime)s - 行数：%(lineno)d - 模块：%(module)s\033[0m"
        )
        logger = logging.getLogger(self.mod_name)
        return logger

    def output_log(self, levelname: str) ->all :
        levels = {
            "info": logging.INFO,
            "debug": logging.DEBUG,
            "warn": logging.WARNING,
            "error": logging.ERROR
        }
        logging.basicConfig(
            level=levels[levelname],
            format=f"%(asctime)s - {sys.argv[0]} - 模块：%(module)s - 行数：%(lineno)d - %(message)s",
            filename="output.log"
        )
        logger = logging.getLogger(self.mod_name)
        return logger


log = LogSet()
l = log.output_log(levelname="debug")
record = l.debug
record("debug")
