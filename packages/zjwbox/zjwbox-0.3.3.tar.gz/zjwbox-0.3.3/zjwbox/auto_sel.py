from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from dataclasses import dataclass
from tqdm import tqdm, trange
import json
from datetime import datetime


@dataclass
class AutoSel(object):
    driver_path: str
    urls: str or list = None
    browser_type: str = None
    css_args: list or tuple = None

    def get_source_page(self, urls: str or list, css_args: list or tuple=None) -> str:
        driver = webdriver.Chrome(executable_path=self.driver_path)
        try:
            driver.get(urls)
            text = driver.page_source
            page_info = driver.get_cookies()
            driver.close()
        except Exception as e:
            print(e)
            driver.close()
        else:
            return text, page_info

    def get_window_page(self, urls: str or list, css_args: list or tuple=None) -> str:
        driver = webdriver.Chrome(executable_path=self.driver_path)
        try:
            driver.get(urls)
            p_texts = []
            p_text = driver.find_elements_by_css_selector(" div > div > p")
            p_text_tqdm = tqdm(p_text)
            for p in p_text_tqdm:
                p_text_tqdm.set_description("正在进行中...")
                if p.text.strip() == '':
                    continue
                p_texts.append(p.text.strip())

        except Exception as e:
            print(e)
            driver.close()
        else:
            return p_texts






# if __name__ == "__main__":
#     driver_path = "D:\\chromedriver\\chromedriver.exe"
#     url = "https://wenku.baidu.com/view/7bb441e6a88271fe910ef12d2af90242a995ab1c.html?fr=aladdin664466&ind=1"
#     a = AutoSel(driver_path=driver_path)
#     text = a.get_window_page(url)
#     print(text)