# yyj
# time:2023/8/12 9:50
import time
from telnetlib import EC

import pandas
import logging
import random
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

OVER_TIME = 5

class test_accounts():



    def get_account_type(self, labels_test_account):

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
        df = pandas.read_csv(labels_test_account)
        datas = df[["labelName", "account_url", "account_sum"]]
        data2 = datas[datas["account_url"].notna()]

        # 遍历account的标签信息
        for indexs in data2.index:
            try:
                labelName = data2.loc[indexs].values[0]
                url = data2.loc[indexs].values[1]
                count = data2.loc[indexs].values[2]
                print(labelName, count)
                if(count > 100):
                    for page in range(0,int(int(count)/100)+1) :
                        time.sleep(1 + random.random())
                        print(page)
                        if(page == 0):
                            if "?subcatid" in url:
                                accountUrl = URL + url + "&size=100&start={}&col=3&order=desc".format(page * 100)
                            else:
                                accountUrl = URL + url + "?&size=100&start={}&col=3&order=desc".format(page * 100)
                            self.driver.get(accountUrl)
                        else:
                            # 模拟滑动到网页底部的JavaScript代码
                            script = """
                            var scrollHeight = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight);
                            var windowHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
                            window.scrollTo(0, scrollHeight - windowHeight);
                            """
                            self.driver.execute_script(script)
                            self.login()
                        time.sleep(3 + random.random())
                        page_sources = self.driver.page_source
                        my_pages = BeautifulSoup(page_sources, 'html.parser')
                        my_pages.prettify()
                        datasNames = []
                        if "?subcatid=1" in url:
                            tbodys = my_pages.find('table', id="table-subcatid-1").find('tbody')
                        elif "?subcatid=2" in url:
                            tbodys = my_pages.find('table',id="table-subcatid-2").find('tbody')
                        elif "?subcatid=3-0" in url:
                            tbodys = my_pages.find('table', id="table-subcatid-3-0").find('tbody')
                        else:
                            tbodys = my_pages.find('tbody')
                        trs = tbodys.find_all('tr')
                        if trs:
                            try:
                                for tr in trs:
                                    # 获取accountTag数据
                                    dataNamedit = {}
                                    account_address = tr.find('a')["data-bs-title"]
                                    tds = tr.find_all('td')
                                    account_nameTag = tds[1].get_text()
                                    print(account_address,account_nameTag)
                                    dataNamedit["account_label"] = labelName
                                    dataNamedit["account_address"] = account_address
                                    dataNamedit["account_nameTag"] = account_nameTag
                                    dataNamedit["account_chain"] = 'Ethereum'
                                    datasNames.append(dataNamedit)
                                df4 = pandas.DataFrame(datasNames)
                                df4.to_csv("account_ETH_2.csv", mode='a', header=False, index=False)
                                print(labelName + "共{}页，第{}页完成".format(int(int(count) / 100) + 1, page + 1))
                                time.sleep(1)
                            except Exception as e:
                                logging.error("获取account>100的%s的labelInfo出错%s" % (labelName, e))
                                errorData = [
                                    {"labelName": labelName, "account_url": url, "account_sum": int(count),
                                     "type": "parser"}]
                                ef = pandas.DataFrame(errorData)
                                ef.to_csv("error_account_ETH_2.csv", mode='a', header=False, index=False)
                else:
                    time.sleep(1+random.random())
                    if "?subcatid" in url:
                        baseUrl = "&size=100&start=0&col=3&order=desc"
                    else:
                        baseUrl = "?&size=100&start=0&col=3&order=desc"
                    accountUrl = URL + url + baseUrl
                    print(accountUrl)
                    self.driver.get(accountUrl)
                    time.sleep(2 + random.random())
                    page_source1 = self.driver.page_source
                    my_page1 = BeautifulSoup(page_source1, 'html.parser')
                    my_page1.prettify()
                    datasName1 = []
                    if "?subcatid=1" in url:
                        tbody1 = my_page1.find('table', id="table-subcatid-1").find('tbody')
                    elif "?subcatid=2" in url:
                        tbody1 = my_page1.find('table', id="table-subcatid-2").find('tbody')
                    elif "?subcatid=3-0" in url:
                        tbody1 = my_page1.find('table', id="table-subcatid-3-0").find('tbody')
                    else:
                        tbody1 = my_page1.find('table', id="table-subcatid-0").find('tbody')
                    trs2 = tbody1.find_all('tr')
                    if trs2:
                        try:
                            for tr2 in trs2:
                                # 获取accountTag数据
                                dataNamedit2 = {}
                                account_address1 = tr2.find('a')["data-bs-title"]
                                tds2 = tr2.find_all('td')
                                account_nameTag11 = tds2[1].get_text()
                                print(account_address1,account_nameTag11)
                                dataNamedit2["account_label"] = labelName
                                dataNamedit2["account_address"] = account_address1
                                dataNamedit2["account_nameTag"] = account_nameTag11
                                dataNamedit2["account_chain"] = 'Ethereum'
                                datasName1.append(dataNamedit2)
                            df4 = pandas.DataFrame(datasName1)
                            df4.to_csv("account_ETH_2.csv", mode='a', header=False, index=False)
                            time.sleep(random.random())
                        except Exception as e:
                            logging.error("获取account<=100的%s的labelInfo出错%s" % (labelName, e))
                            errorData = [
                                {"labelName": labelName, "account_url": url, "account_sum": int(count), "type": "parser"}]
                            ef = pandas.DataFrame(errorData)
                            ef.to_csv("error_account_ETH_2.csv", mode='a', header=False, index=False)
            except Exception as e:
                logging.error("%s获取出现错误:%s" % (labelName, e))
                errorData = [{"labelName": labelName, "account_url": url, "account_sum": int(count), "type": "csv"}]
                ef = pandas.DataFrame(errorData)
                ef.to_csv("error_account_ETH_2.csv", mode='a', header=False, index=False)

    def login(self):
        try:
            ele0= "/html[@id='html']/body[@id='body']/main[@id='content']/section[@class='container-xxl pt-5 pb-12']/div[@class='card']/div[@id='tabContent']/div[@id='subcattab-0']/div[@id='paywall_mask_table-subcatid-0']/div[@id='table-subcatid-0_wrapper']/div[@class='card-footer d-flex flex-wrap justify-content-between align-items-center gap-3 bottomdivdt']/div[2]/div[@id='table-subcatid-0_paginate']/ul[@class='pagination pagination-sm mb-0']/li[@id='table-subcatid-0_next']/a[@class='page-link px-3']"
            ele1 = "/html[@id='html']/body[@id='body']/main[@id='content']/section[@class='container-xxl pt-5 pb-12']/div[@class='card']/div[@id='tabContent']/div[@id='subcattab-1']/div[@id='paywall_mask_table-subcatid-1']/div[@id='table-subcatid-1_wrapper']/div[@class='card-footer d-flex flex-wrap justify-content-between align-items-center gap-3 bottomdivdt']/div[2]/div[@id='table-subcatid-1_paginate']/ul[@class='pagination pagination-sm mb-0']/li[@id='table-subcatid-1_next']/a[@class='page-link px-3']"
            ele2 = "/html[@id='html']/body[@id='body']/main[@id='content']/section[@class='container-xxl pt-5 pb-12']/div[@class='card']/div[@id='tabContent']/div[@id='subcattab-2']/div[@id='paywall_mask_table-subcatid-2']/div[@id='table-subcatid-2_wrapper']/div[@class='card-footer d-flex flex-wrap justify-content-between align-items-center gap-3 bottomdivdt']/div[2]/div[@id='table-subcatid-2_paginate']/ul[@class='pagination pagination-sm mb-0']/li[@id='table-subcatid-2_next']"
            ele3 = "/html[@id='html']/body[@id='body']/main[@id='content']/section[@class='container-xxl pt-5 pb-12']/div[@class='card']/div[@id='tabContent']/div[@id='subcattab-3-0']/div[@id='paywall_mask_table-subcatid-3-0']/div[@id='table-subcatid-3-0_wrapper']/div[@class='card-footer d-flex flex-wrap justify-content-between align-items-center gap-3 bottomdivdt']/div[2]/div[@id='table-subcatid-3-0_paginate']/ul[@class='pagination pagination-sm mb-0']/li[@id='table-subcatid-3-0_next']/a[@class='page-link px-3']/i[@class='fa fa-chevron-right small']"

            try:
                ele0_click = self.driver.find_element(By.XPATH,ele0)
                ele0_click.click()
            except NoSuchElementException:
                try:
                    ele1_click = self.driver.find_element(By.XPATH, ele1)
                    ele1_click.click()
                except NoSuchElementException:
                    try:
                        ele2_click = self.driver.find_element(By.XPATH, ele2)
                        ele2_click.click()
                    except NoSuchElementException:
                        try:
                            ele3_click = self.driver.find_element(By.XPATH, ele3)
                            ele3_click.click()
                        except NoSuchElementException:
                            print("subcatid类型未知")

        except Exception as e:
            logging.error(e)




if __name__ == '__main__':
    ll = test_accounts()
    ll.get_account_type("labels_20230811_ETH_Accounts.csv")
    # ll.get_account_type("error_account_ETH_2.csv")

