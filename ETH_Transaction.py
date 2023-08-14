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
from selenium.webdriver.support import expected_conditions as EC
import math

OVER_TIME = 5

class test_transactions():


    def get_transaction_Info(self, labels_test_transaction):

        # 每次启动之前都需手动登录etherscan，先完成站点验证!!!
        chrome_user_data_dir = r"user-data-dir=C:\Users\yongjie.yu\AppData\Local\Google\Chrome\User Data"
        chrome_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(chrome_user_data_dir)
        chrome_options.add_experimental_option('detach', True)
        # 应对反爬：无头模式需要user-agent
        chrome_options.add_argument(f'user-agent={chrome_user_agent}')
        chrome_options.add_argument('window-size=1920x3000')
        chrome_options.add_argument('--ignore-certificate-errors')
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--hide-scrollbars')
        s = Service(
            executable_path=r'C:\Program Files\JetBrains\PyCharm Community Edition 2023.1.1\bin\chromedriver.exe')
        self.driver = webdriver.Chrome(service=s, options=chrome_options)
        self.driver.implicitly_wait(OVER_TIME)
        self.driver.maximize_window()
        self.driver.get("https://etherscan.io/labelcloud")
        URL = "https://etherscan.io"
        df = pandas.read_csv(labels_test_transaction, na_values=[""])
        datas = df[["labelName", "transaction_url", "transaction_sum"]]
        data2 = datas[datas["transaction_url"].notna()]
        #遍历accounts的标签信息
        for indexs in data2.index:
            try:
                # labelName = data2.loc[indexs].values[0]
                labelName = "EigenPhi"
                url = data2.loc[indexs].values[1]
                count = data2.loc[indexs].values[2]
                print(indexs,labelName,count)
                # 如果标签中的transaction数量>= 100,需要单独处理
                if int(count) > 100:
                    print("186,EigenPhi,,,,,/blocks/label/eigenphi,1173911,/txs/label/eigenphi,5560530")
                    time.sleep(1 + random.random())
                    for page in range(0 ,int(int(count) / 100) + 1):
                        time.sleep(0.1 + random.random())
                        pages = int(int(count) / 100) + 1
                        if(page == 0):
                            # self.login()
                            # time.sleep(2 + random.random())
                            # # transactionUrl = URL + url + "?size=100&start=%s#" % (page * 100)
                            # # print(transactionUrl,labelName)
                            # #self.driver.get(transactionUrl)
                            # # 设置等待时间，这里设置为20秒，可以根据网页加载速度适当调整
                            # wait = WebDriverWait(self.driver, 20)
                            # # 等待直到某个元素出现，可以根据具体网页的加载情况来选择等待的元素
                            # element = wait.until(EC.presence_of_element_located((By.XPATH, "//i[@class='far fa-eye']")))
                            # print(page)
                            # if(page % 10 == 0):
                            #     time.sleep(5)
                            self.driver.get("https://etherscan.io/txs/label/eigenphi?size=100&start=0")
                            time.sleep(60)
                        else:
                            self.login()
                            time.sleep(3 + random.random())
                            page_source = self.driver.page_source
                            my_page1 = BeautifulSoup(page_source, 'html.parser')
                            my_page1.prettify()
                            my_table = my_page1.find('table', class_="table table-hover mb-0 dataTable no-footer")
                            tbodys1 = my_table.find('tbody',class_="align-middle text-nowrap")
                            datasName1 = []
                            trs1 = tbodys1.find_all('tr')
                            if trs1:
                                try:
                                    for tr1 in trs1:
                                        #获取Account数据
                                        dataNamedit1 = {}
                                        tds = tr1.find_all('td')
                                        transaction_address = tds[1].find('a').get_text()
                                        # transaction_address = tr1.find('a')["myFnExpandBox_searchVal"]
                                        dataNamedit1["transaction_label"] = labelName
                                        dataNamedit1["transaction_address"] = transaction_address
                                        dataNamedit1["transaction_chain"] = "Ethereum"
                                        datasName1.append(dataNamedit1)
                                    df2 = pandas.DataFrame(datasName1)
                                    df2.to_csv("transaction_20230814_ETH.csv", mode='a',header=False,index=False)
                                    print('共'+str(pages)+'页，第'+str(page+1)+'完成')
                                    logging.info('共%s页，第%s页完成' %(pages,page+1))
                                except Exception as e:
                                    logging.error(e)
                                    errorData = [{"labelName": labelName, "account_url": url, "account_sum": int(count), "type": "parser"}]
                                    ef = pandas.DataFrame(errorData)
                                    ef.to_csv("./ETHLabelInfo/error_transactions_ETH.csv", mode='a', header=False,index=False)
                            time.sleep(0.5 + random.random())
                            if(page % 20 ==0):
                                time.sleep(5)
                else:
                    time.sleep(1 + random.random())
                    paseUrl = URL + url + "?size=100&start=0&col=3&order=desc"
                    print(paseUrl)
                    self.driver.get(paseUrl)
                    # 设置等待时间，这里设置为10秒，可以根据网页加载速度适当调整
                    wait = WebDriverWait(self.driver, 10)
                    # # 等待直到某个元素出现，可以根据具体网页的加载情况来选择等待的元素
                    # element = wait.until(EC.presence_of_element_located((By.XPATH, "//i[@class='far fa-file-alt text-secondary me-1']")))
                    time.sleep(3)
                    page_source = self.driver.page_source
                    my_page = BeautifulSoup(page_source, 'html.parser')
                    my_page.prettify()
                    print(my_page)
                    my_table1 = my_page.find('table', class_="table table-hover mb-0 dataTable no-footer")
                    tbodys = my_table1.find('tbody', class_="align-middle text-nowrap")
                    print(tbodys)
                    datasName2 = []
                    trs2 = tbodys.find_all('tr')
                    if trs2:
                        try:
                            for tr2 in trs2:
                                # 获取accountTag数据
                                dataNamedit2 = {}
                                transaction_address = tr2.find('a',class_="myFnExpandBox_searchVal")["href"].split("/")[2]
                                dataNamedit2["transaction_label"] = labelName
                                dataNamedit2["transaction_address"] = transaction_address
                                dataNamedit2["transaction_chain"] = "Ethereum"
                                datasName2.append(dataNamedit2)
                            df4 = pandas.DataFrame(datasName2)
                            df4.to_csv("transaction_20230727_nameTagInfo_ETH.csv", mode='a', header=False, index=False)
                            time.sleep(random.random())
                        except Exception as e:
                            logging.error("获取account<100的%s的Name出错%s" %(labelName, e))
                            errorData = [{"labelName": labelName, "transaction_url": url, "transaction_sum": int(count),  "type": "parser"}]
                            ef = pandas.DataFrame(errorData)
                            ef.to_csv("error_transactions_imgInfo_ETH.csv", mode='a', header=False,index=False)
            except Exception as e:
                logging.error("%s获取出现错误:%s" % (labelName, e))
                errorData = [{"labelName":labelName, "transaction_url": url, "transaction_sum": int(count), "type":"csv"}]
                ef = pandas.DataFrame(errorData)
                ef.to_csv("error_transactions_imgInfo_ETH.csv",mode='a',header=False,index=False)


    def login(self):
        ele = "/html[@id='html']/body[@id='body']/main[@id='content']/section[@class='container-xxl pt-5 pb-12']/div[@id='ContentPlaceHolder1_divTransactionsByLabel']/div[@class='card']/div[@id='tblTxnsByLabelWrapper']/div[@id='tableTxnsByLabel_wrapper']/div[@class='d-flex flex-wrap align-items-center justify-content-between gap-3 p-4 text-dark']/div[@id='tableTxnsByLabel_paginate']/ul[@class='pagination pagination-sm mb-0']/li[@id='tableTxnsByLabel_next']/a[@class='page-link px-3']"
        if self.driver.find_element(By.XPATH,ele):
            self.driver.find_element(By.XPATH,ele).click()








if __name__ == '__main__':
    ll = test_transactions()

    # 遍历transaction标签csv文件，获取所有transaction
    print("开始获取transaction别名和图片URL：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "**********************")
    ll.get_transaction_Info("transaction_eth.csv")
    print("结束获取：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "**********************")




