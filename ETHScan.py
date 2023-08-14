import time
import pandas
import logging
import random
from bs4 import BeautifulSoup
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import requests
from selenium.webdriver.support.wait import WebDriverWait

# yyj
# time:2023/8/11 21:51

class Label():

    def label_page_list(self):
        # 每次启动之前都需手动登录etherscan，先完成站点验证!!!
        chrome_user_data_dir = r"user-data-dir=C:\Users\yuyon\AppData\Local\Google\Chrome\User Data"
        chrome_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(chrome_user_data_dir)
        chrome_options.add_experimental_option('detach', True)
        # 应对反爬：无头模式需要user-agent
        chrome_options.add_argument(f'user-agent={chrome_user_agent}')
        chrome_options.add_argument('window-size=1920x3000')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--hide-scrollbars')
        s = Service(
            executable_path=r'D:\PyC\PyCharm Community Edition 2022.2.3\bin\chromedriver.exe')
        self.driver = webdriver.Chrome(service=s, options=chrome_options)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

        imgUrl = "https://etherscan.io/labelcloud"
        self.driver.get(imgUrl)

        page_source = self.driver.page_source
        my_page1 = BeautifulSoup(page_source, 'html.parser')
        my_page1.prettify()

        datas = []
        container = my_page1.find_all('div', class_='col-md-4 col-lg-3 mb-3 secondary-container')
        print(container)

        for data in container:
            lableList = {}
            lableList["labelName"] = "".join(data.button.span.get_text().split(" ")[0:-1])
            hrefs = data.find_all('a')
            for href in hrefs:
                name = href.get_text().split(" ")[0]
                if name.find("Transactions") != -1:
                    transactions_url = href["href"]
                    transaction_sum = href.get_text().split(" ")[1].strip("()")
                    lableList["transaction_url"] = transactions_url
                    lableList["transaction_sum"] = transaction_sum
                elif name.find("Accounts") != -1:
                    account_url = href["href"]
                    account_sum = href.get_text().split(" ")[1].strip("()")
                    lableList["account_url"] = account_url
                    lableList["account_sum"] = account_sum
                elif name.find("Tokens") != -1:
                    tokens_url = href["href"]
                    tokens_sum = href.get_text().split(" ")[1].strip("()")
                    lableList["tokens_url"] = tokens_url
                    lableList["tokens_sum"] = tokens_sum
            datas.append(lableList)
        print("datas=", datas)
        df = pandas.DataFrame(datas)
        return df

if __name__ == '__main__':
    ll=Label()
    result=ll.label_page_list()
    result.to_csv("labels_20230811_ETH.csv")
