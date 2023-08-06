import requests, re, wget, zipfile, os
from pprint import pprint


def update_driver(os_type: str="win32", file_path: str=None, zip_path: str=None, del_zip: str=False) -> None:
    url = "http://chromedriver.storage.googleapis.com/?delimiter=/&prefix="
    session = requests.Session()
    resp = session.get(url)
    text = resp.text

    pattern = r"<Prefix>(\d.*?)/"
    versions = re.findall(pattern=pattern, string=text)
    pprint(versions)
    print(f"一共找到{len(versions)}个版本，最新版本{versions[-1]}")
    while True:
        change_version = input("请选择要更新的版本：")
        if change_version in versions:
            print(f"已选择：{change_version} !")
            break
        else:
            print(f"无该版本：{change_version}，请重新输入！")

    if not zip_path:
        zip_path = "chromedriver.zip"
    wget.download(f"http://chromedriver.storage.googleapis.com/{change_version}/chromedriver_{os_type}.zip", out=zip_path)
    print(f"zip文件保存成功！路径：{os.getcwd()}{os.path.sep}{zip_path}")
    zfile = zipfile.ZipFile(zip_path, "r")
    if file_path:
        zfile.extractall(path=file_path)
    else:
        zfile.extractall()
    zfile.close()
    if del_zip:
        os.remove(os.getcwd() + f"{os.path.sep}{zip_path}")
        print(f"zip文件已删除！")
    print(f"exe文件保存成功！路径：{file_path}" + f"{os.path.sep}" + "chromedriver.exe")




__name__ = ["update_driver"]

if __name__ == "__main__":
    update_driver(del_zip=True, file_path="D:\\test")