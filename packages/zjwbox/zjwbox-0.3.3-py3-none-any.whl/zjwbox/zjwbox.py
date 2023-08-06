from dataclasses import dataclass
from collections import Counter
from zjwbox.boxtools.alert_exit import alertExit
from datetime import datetime


@dataclass
class Infer(object):
    data_type: str
    
    def __str__(self):
        info =         """
        welcome you!
        This is a class that improve infer!
        You must give it a arg to str type, "list", "tuple" or "set".
        """
        return info
    
    def __getitem__(self, key):
        if len(str(key)) < 2:
            print("语法错误：输入格式数不能少于2！")
            return
        if isinstance(key, tuple) and len(key) in (2, 3, 4) and (key[2] is Ellipsis or key[1] is Ellipsis or key[3] is Ellipsis):
            if key[1] is Ellipsis:
                basic_infer = [i for i in range(key[0], key[-1] + 1)]
            elif key[3] is Ellipsis:
                basic_infer = [i for i in range(key[0], key[-1] + 1, key[1] - key[0])]
            else:
                basic_infer = [i for i in range(key[0], key[-1] + 1, key[1] - key[0])]
            
            if self.data_type == "list":
                return basic_infer
            if self.data_type == "tuple":
                return tuple(basic_infer)
            if self.data_type == "set":
                return set(basic_infer)
        timers = Counter(self.data_type).most_common()
        for timer in timers:
            if 2 in timer:
                print(f"请检查参数: {self.data_type}\n参考参数：'list', 'tuple', 'set'！")
                return
        if len(self.data_type) < 3 or len(self.data_type) > 5:
            print(f"请检查参数: {self.data_type}\n参考参数：'list', 'tuple', 'set'！")
        else:
            print(None)
                

alertExit()


# if __name__ == "__main__":
#     p = Infer("set")
#     print( p[1, 5,  ...,100] )

