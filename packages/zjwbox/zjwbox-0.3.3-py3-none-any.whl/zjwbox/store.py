from dataclasses import dataclass
import pymongo, pymysql, redis
from tqdm import tqdm, trange
import csv, openpyxl
from collections.abc import Iterable
from threading import Lock
from zjwbox.boxtools.log_set import LogSet
from datetime import datetime



"""
welcome you !
This is a class about store data !
You might use it store many different type for your data
For example, txt, Csv, Excel, a kind of Databases !
You should give it some args, text of data, path of file and name of file,
It is necessary to some args, your data in text, path of file, filename.
"""


@dataclass
class Store(object):
    text: list or dict
    path: str
    filename:str
    debug_mode: str = "no"
    logger: object = LogSet().debug_log(levelname=debug_mode)
    log: object = LogSet().output_log(levelname="debug")
    debug: object = logger.warning
    warn:object = logger.info
    error:object = logger.debug
    record:object = log.info

    _instance_lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Store, "_instance"):
            with Store._instance_lock:
                if not hasattr(Store, "_instance"):
                    Store._instance = object.__new__(cls)  
        return Store._instance


    def __str__(self) -> str:
        info = """
                This is a class about store data !
                You able use it store many different type for your data !
                For example, txt, Csv, Excel, a kind of Databases !
                """
        return info


    """
    Save to your TXT !
    you may give some choice args, for example,  encode of char, 
    even can change is_mark that decide read, write or add to !
    """
    def to_txt(self, encode: str="utf-8", is_mark=True ) -> all:
        if isinstance(self.text, list):
            words, count = 0, 0
            mode = "a+"
            if is_mark:
                mode = "w+"
            with open(f"{self.path}/{self.filename}", mode=mode, encoding=encode) as f:
                for i in tqdm(self.text):
                    f.writelines(i)
                    count += 1
                    words += len(i)
                    self.debug(words)
                    self.record(words)
            print(f"保存完成！location of file：{self.path}/{self.filename}，共{count}行，{words}字！")
        else:
            print("TypeErorr: text must be list !")


    """
    Save to your CSV !
    you can give some choice args for this function, for example, mode to read and write, 
    if your datas is dict or set of dict, you may give a arg of headers(title in csv),
    you even can change is_single that deal most datas !
    """
    def to_csv(self, mode="w+", encode: str="utf-8", is_single=True, headers=None)-> None :
        if ( isinstance(self.text, list) and not isinstance(self.text[0], dict) ) or isinstance(self.text[0], list):
            if mode == "r":
                with open(f"{self.path}/{self.filename}", mode=mode, encoding=encode) as f:
                    reader = csv.reader(f)
                    for row in reader:
                        print(row)
                        self.record(row)
            with open(f"{self.path}/{self.filename}", mode=mode, encoding=encode, newline="") as f:
                writer = csv.writer(f)
                if isinstance(self.text[0], list):
                    if is_single:
                        for t in tqdm(self.text):
                            writer.writerow(t)
                            self.debug(t)
                            self.record(t)
                            tqdm(self.text).set_description("正在写入中！")
                elif isinstance(self.text, list):
                    if is_single:
                        for t in tqdm(self.text):
                            writer.writerow(t)
                            self.debug(t)
                            self.record(t)
                            tqdm(self.text).set_description("正在写入中！")
                    else:
                        for t in tqdm(self.text):
                            writer.writerows(t)
                            self.debug(t)
                            self.record(t)
                            tqdm(self.text).set_description("正在写入中！")
                    print("写入完成！")

        elif isinstance(self.text, dict) or isinstance(self.text[0], dict):
            if mode == "r":
                with open(f"{self.path}/{self.filename}", mode=mode, encoding=encode) as f:
                    reader = csv.reader(f)
                    for row in reader:
                        print(row)
                        self.record(row)
            else:
                with open(f"{self.path}/{self.filename}", mode=mode, encoding=encode, newline="") as f:
                    Dictwriter = csv.DictWriter(f, headers)
                    Dictwriter.writeheader()
                    if  isinstance(self.text[0], dict):
                        if is_single:
                            for d in tqdm(self.text):
                                Dictwriter.writerow(d)
                                self.debug(d)
                                self.record(d)
                                tqdm(self.text).set_description("正在写入中！")
                        else:
                            for d in tqdm(self.text):
                                Dictwriter.writerows(d)
                                self.debug(d)
                                self.record(d)
                                tqdm(self.text).set_description("正在写入中！")
                        print("写入完成！")
                    else:
                        if is_single:
                            Dictwriter.writerow(self.text)
                            print("写入完成！")
                        else:
                            for row in tqdm(self.text):
                                Dictwriter.writerows(row)
                                self.record(row)
                                self.debug(row)
                                tqdm(self.text).set_description("正在写入中！")
                            print("写入完成！")

        else:
            print("TypeErorr: text must be list or dict !")


    """
    Save to your Excel !
    This function have a necessary arg to sheet_name .
    of couser, you also give some choice args, for example, mode to read and write, 
    excel that row, column and value,
    you even can change is_single that deal most datas !
    """
    def ente_excel(func) -> all:
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
        return wrapper

    @ente_excel
    def to_excel(
        self, sheet_name: str, mode="w", row=None, column=None, value=None, own=False, is_single=False
    ) -> None:
        wb = openpyxl.Workbook()
        sh = wb.create_sheet(sheet_name)
        if mode == "w":
            if not isinstance(self.text[0], Iterable):
                if own:
                    row, column, value = self.text
                    self.debug(row+"--"+column+"--"+value)
                    self.record(row+"--"+column+"--"+value)
                    sh.cell(row=row, column=column, value=value)
                    wb.save( f"{self.path}/{self.filename}" )
                    wb.close()
                    print("保存成功！")
                    return
                else:
                    tqdm_text = tqdm(self.text)
                    for t in tqdm_text:
                        row, column, value = t
                        self.debug(row+"--"+column+"--"+value)
                        self.record(row+"--"+column+"--"+value)
                        sh.cell(row=row, column=column, value=value)
                        tqdm_text.set_description("正在保存中！")
                    wb.save( f"{self.path}/{self.filename}" )
                    wb.close()
                    print("保存成功！")
                    return

        wb = openpyxl.load_workbook(f"{self.path}/{self.filename}")
        sh = wb[sheet_name]
        #按行读取数据转化为列表
        rows_data = list(sh.rows)
        self.record(rows_data)
        self.debug(rows_data)
        # 获取表单的表头信息
        titles = []
        for title in rows_data[0]:
            titles.append(title.value)
            self.warn("title.value："+title.value)
            self.record("title.value："+title.value)
        cases = []
        for case in rows_data[1:]:
            data = []
            for cell in case: 
                data.append(cell.value)
                if isinstance(cell.value,str):
                    data.append(cell.value)
                    self.warn("cell.value："+cell.value)
                    self.record("cell.value："+cell.value)
                else:
                    data.append(cell.value)
                    self.warn("cell.value："+cell.value)
                    self.record("cell.value："+cell.value)
                case_data = dict(  list (zip(titles,data) )  )
                cases.append(case_data)
                self.warn("case_data："+case_data)
                self.record("case_data："+case_data)
        return cases


    def to_db(self, db_type: str, login_data: dict, sql=None) -> all:
        # mysql
        if db_type == "mysql": 
            db = pymysql.connect(
                host=login_data["host"], 
                port=login_data["port"],
                user=login_data["user"],
                password=login_data["password"],
                database=login_data["database"],
                charset=login_data["charset"]
            )
            cursor = db.cursor()
            if sql:
                SqlSCInsert = sql
                try:
                    cursor.execute(SqlSCInsert)
                    # 提交到数据库执行
                    db.commit()
                    print("完成！")
                except Exception as e:
                    raise e
                # 如果发生错误则回滚
                    db.rollback()
                cursor.close()
                db.close()
            else:
                return db

        # mongodb
        elif db_type == "mongodb":
            try:
                client = pymongo.MongoClient(login_data["host"],  login_data["port"])
                mydb = login_data["database"]
                if login_data["password"]:
                    db = client.admin    # 连接系统默认数据库admin
                    db.authenticate("用户名", "密码")
                else:
                    db = client.mydb
                    myset = db.login_data['set']
                    print("\033[1;32m连接成功！\033[0m")
                    result = myset.sql
                    return result
            except Exception as e:
                print("\033[1;31m连接失败！\033[0m")
                print(f"错误：{e}")
            
        elif db_type == "redis":
            if not login_data:
                try:
                    conn =redis.Redis(
                        host=login_data["host"],
                        port=login_data["port"],
                        password=login_data["password"]
                    )
                    print("\033[1;32m连接成功！\033[0m")
                except Exception as e:
                    print("\033[1;31m连接失败！\033[0m")
                    print(f"错误：{e}")
            else:
                try:
                    conn =redis.Redis(
                        host=login_data["host"],
                        port=login_data["port"],
                        db=login_data.get("database", 0)
                    )
                    print("\033[1;32m连接成功！\033[0m")
                except Exception as e:
                    print("\033[1;31m连接失败！\033[0m")
                    print(f"错误：{e}")
            return conn

