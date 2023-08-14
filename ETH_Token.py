# yyj
# time:2023/8/12 9:50
import time
from telnetlib import EC

import pandas
import logging
import random
from bs4 import BeautifulSoup
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

OVER_TIME = 5

class test_tokens():



    def get_token_type(self, labels_test_token):

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
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--hide-scrollbars')
        s = Service(
            executable_path=r'D:\PyC\PyCharm Community Edition 2022.2.3\bin\chromedriver.exe')
        self.driver = webdriver.Chrome(service=s, options=chrome_options)
        self.driver.implicitly_wait(OVER_TIME)
        self.driver.maximize_window()
        self.driver.get("https://etherscan.io/labelcloud")
        URL = "https://etherscan.io"
        df = pandas.read_csv(labels_test_token)
        datas = df[["labelName", "tokens_url", "tokens_sum"]]
        data2 = datas[datas["tokens_url"].notna()]

        # 遍历tokens的标签信息
        for indexs in data2.index:
            try:
                labelName = data2.loc[indexs].values[0]
                url = data2.loc[indexs].values[1]
                count = data2.loc[indexs].values[2]
                print(labelName, count)
                if(count > 100):
                    for page in range(0,int(int(count)/100)+1) :
                        time.sleep(2 + random.random())
                        print(page)
                        if(page == 0):
                            if "?subcatid" in url:
                                tokensUrl = URL + url + "&size=100&start={}&col=3&order=desc".format(page * 100)
                            else:
                                tokensUrl = URL + url + "?&size=100&start={}&col=3&order=desc".format(page * 100)
                            self.driver.get(tokensUrl)
                        else:
                            self.login()
                        # # 最大等待时间为10秒
                        # wait = WebDriverWait(self.driver, 10)
                        # # 等待直到元素可见
                        # element = wait.until(EC.presence_of_element_located((By.ID, 'linkIcon_1')))
                        time.sleep(4)
                        page_sources = self.driver.page_source
                        my_pages = BeautifulSoup(page_sources, 'html.parser')
                        my_pages.prettify()
                        datasNames = []
                        tbodys = my_pages.find('tbody')
                        trs = tbodys.find_all('tr')
                        if trs:
                            try:
                                for tr in trs:
                                    # 获取tokenTag数据
                                    dataNamedit = {}
                                    token_address = tr.find('a')["data-bs-title"]
                                    token_nameTag1 = tr.find('span', class_="text-truncate")
                                    token_nameTag2 = tr.find('span', class_="text-muted")
                                    token_nameTag3 = tr.find('span', class_="hash-tag text-truncate")
                                    dataNamedit["token_label"] = labelName
                                    dataNamedit["token_address"] = token_address
                                    if token_nameTag1 is None :
                                        if token_nameTag2 is  None:
                                            if token_nameTag3 is not None:
                                                dataNamedit["token_nameTag"] = token_nameTag3.get_text()
                                        else:
                                            dataNamedit["token_nameTag"] = token_nameTag3.get_text() + token_nameTag2.get_text()
                                    else:
                                        if token_nameTag2 is None:
                                            dataNamedit["token_nameTag"] = token_nameTag1.get_text()
                                        else:
                                            dataNamedit["token_nameTag"] = token_nameTag1.get_text() + token_nameTag2.get_text()
                                    dataNamedit["token_chain"] = 'Ethereum'
                                    datasNames.append(dataNamedit)
                                df4 = pandas.DataFrame(datasNames)
                                df4.to_csv("tokens_ETH_2.csv", mode='a', header=False, index=False)
                                print(labelName + "共{}页，第{}页完成".format(int(int(count) / 100) + 1, page + 1))
                                time.sleep(1)
                            except Exception as e:
                                logging.error("获取token<=100的%s的Img和Name出错%s" % (labelName, e))
                                errorData = [
                                    {"labelName": labelName, "token_url": url, "token_sum": int(count),
                                     "type": "parser"}]
                                ef = pandas.DataFrame(errorData)
                                ef.to_csv("error_tokens_ETH_2.csv", mode='a', header=False, index=False)
                else:
                    time.sleep(1+random.random())
                    if "?subcatid" in url:
                        baseUrl = "&size=100&start=0&col=3&order=desc"
                    else:
                        baseUrl = "?&size=100&start=0&col=3&order=desc"
                    tokenUrl = URL + url + baseUrl
                    print(tokenUrl)
                    self.driver.get(tokenUrl)
                    time.sleep(3)
                    page_source1 = self.driver.page_source
                    my_page1 = BeautifulSoup(page_source1, 'html.parser')
                    my_page1.prettify()
                    datasName1 = []
                    tbody1 = my_page1.find('tbody')
                    trs2 = tbody1.find_all('tr')
                    if trs2:
                        try:
                            for tr2 in trs2:
                                # 获取tokenTag数据
                                dataNamedit2 = {}
                                token_address1 = tr2.find('a')["data-bs-title"]
                                token_nameTag11 = tr2.find('span', class_="text-truncate").get_text()
                                token_nameTag21 = tr2.find('span', class_="text-muted").get_text()
                                token_nameTag31 = tr2.find('span', class_="hash-tag text-truncate").get_text()
                                dataNamedit2["token_label"] = labelName
                                dataNamedit2["token_address"] = token_address1
                                if token_nameTag11 is None:
                                    if token_nameTag21 is None:
                                        if token_nameTag31 is not None:
                                            dataNamedit2["token_nameTag"] = token_nameTag31
                                    else:
                                        dataNamedit2["token_nameTag"] = token_nameTag31 + token_nameTag21
                                else:
                                    if token_nameTag21 is None:
                                        dataNamedit2["token_nameTag"] = token_nameTag11
                                    else:
                                        dataNamedit2["token_nameTag"] = token_nameTag11 + token_nameTag21
                                dataNamedit2["token_chain"] = 'Ethereum'
                                datasName1.append(dataNamedit2)
                            df4 = pandas.DataFrame(datasName1)
                            df4.to_csv("tokens_ETH_2.csv", mode='a', header=False, index=False)
                            time.sleep(random.random())
                        except Exception as e:
                            logging.error("获取token<=100的%s的Img和Name出错%s" % (labelName, e))
                            errorData = [
                                {"labelName": labelName, "token_url": url, "token_sum": int(count), "type": "parser"}]
                            ef = pandas.DataFrame(errorData)
                            ef.to_csv("error_tokens_ETH_2.csv", mode='a', header=False, index=False)
            except Exception as e:
                logging.error("%s获取出现错误:%s" % (labelName, e))
                errorData = [{"labelName": labelName, "token_url": url, "token_sum": int(count), "type": "csv"}]
                ef = pandas.DataFrame(errorData)
                ef.to_csv("error_tokens_ETH_2.csv", mode='a', header=False, index=False)

    def login(self):
        ele = "/html[@id='html']/body[@id='body']/main[@id='content']/section[@class='container-xxl pt-5 pb-12']/div[@id='ContentPlaceHolder1_divTokenByLabels']/div[@class='tab-content']/div[@id='tab-0-content']/div[@class='card']/div[@class='table-responsive']/div[@id='table-subcatid-0_wrapper']/div[@class='d-flex flex-wrap align-items-center justify-content-between gap-3 p-4 text-dark']/div[@id='table-subcatid-0_paginate']/ul[@class='pagination pagination-sm mb-0']/li[@id='table-subcatid-0_next']/a[@class='page-link px-3']/i[@class='fas fa-chevron-right small']"
        if self.driver.find_element(By.XPATH,ele):
            self.driver.find_element(By.XPATH,ele).click()





if __name__ == '__main__':
    ll = test_tokens()
    ll.get_token_type("labels_20230811_ETH.csv")

    # # 遍历所有token的URL，下载图片到本地存储
    # print("开始下载图片："+ time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) +"**********************")
    # ll.get_token_Img("tokens_imgInfo_ETH.csv")
    # print("结束下载：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "**********************")
