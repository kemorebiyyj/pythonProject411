# # yyj
# # time:2023/7/27 21:33
# import time
# import pandas
# import logging
# import random
# from bs4 import BeautifulSoup
# from selenium.webdriver.chrome import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import os
# import requests
# from selenium.webdriver.support.wait import WebDriverWait
#
# OVER_TIME = 5
#
# class test_tokens():
#
#
#
#     def get_token_type(self, labels_test_token):
#
#         # 每次启动之前都需手动登录etherscan，先完成站点验证!!!
#         chrome_user_data_dir = r"user-data-dir=C:\Users\yuyon\AppData\Local\Google\Chrome\User Data"
#         chrome_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
#         chrome_options = webdriver.ChromeOptions()
#         chrome_options.add_argument(chrome_user_data_dir)
#         chrome_options.add_experimental_option('detach', True)
#         # 应对反爬：无头模式需要user-agent
#         chrome_options.add_argument(f'user-agent={chrome_user_agent}')
#         chrome_options.add_argument('window-size=1920x3000')
#         chrome_options.add_argument('--ignore-certificate-errors')
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--disable-gpu')
#         # chrome_options.add_argument('--hide-scrollbars')
#         s = Service(
#             executable_path=r'D:\PyC\PyCharm Community Edition 2022.2.3\bin\chromedriver.exe')
#         self.driver = webdriver.Chrome(service=s, options=chrome_options)
#         self.driver.implicitly_wait(OVER_TIME)
#         self.driver.maximize_window()
#         URL = "https://etherscan.io"
#         df = pandas.read_csv(labels_test_token)
#         datas = df[["labelName", "tokens_url", "tokens_sum"]]
#         data2 = datas[datas["tokens_url"].notna()]
#
#         # 遍历tokens的标签信息
#         for indexs in data2.index:
#             try:
#                 labelName = data2.loc[indexs].values[0]
#                 url = data2.loc[indexs].values[1]
#                 count = data2.loc[indexs].values[2]
#                 imgUrl = "https://etherscan.io"
#                 print(indexs, labelName, count)
#                 logging.info(indexs, labelName)
#                 baseUrl = "?&size=100&start=7&col=3&order=desc"
#                 tokenUrl = URL + url + baseUrl
#                 print(tokenUrl)
#                 page_source = self.driver.page_source
#                 my_page1 = BeautifulSoup(page_source, 'html.parser')
#                 my_page1.prettify()
#                 tbodys1 = my_page1.find('tbody')
#                 datasImg1 = []
#                 datasName1 = []
#                 main1 = tbodys1.find('a')["nav-link active"]
#                 other1 = tbodys1.find('a')["nav-link"]
#                 if main1 is not None :
#                 df1 = pandas.DataFrame(datasImg1)
#                 df1.to_csv("tokens_20230727_imgInfo_ETH.csv", mode='a', header=False, index=False)
#                 df2 = pandas.DataFrame(datasName1)
#                 df2.to_csv("tokens_20230727_nameTagInfo_ETH.csv", mode='a', header=False, index=False)
#                 print('共' + str(pages) + '页，第' + str(page + 1) + '完成')
#                 logging.info('共%s页，第%s页完成' % (pages, page + 1))
#                             except Exception as e:
#                                 logging.error("获取token>100的%s的Img和Name出错%s" % (labelName, e))
#                                 errorData = [{"labelName": labelName, "token_url": url, "token_sum": int(count),
#                                               "type": "parser"}]
#                                 ef = pandas.DataFrame(errorData)
#                                 ef.to_csv("error_tokens_imgInfo_ETH.csv", mode='a', header=False, index=False)
#                         time.sleep(0.1 + random.random())
#                 else:
#                     time.sleep(0.5 + random.random())
#                     paseUrl = URL + url + "?subcatid=0&size=50&start=0&col=3&order=desc"
#                     self.driver.get(paseUrl)
#                     # # 模拟滚动滑轮到网页最下面
#                     # # 可以根据需要调整滚动次数，这里使用了3次滚动来示例
#                     # scroll_count = 3
#                     # for i in range(scroll_count):
#                     #     js = "window.scrollTo(0, document.body.scrollHeight)"
#                     #     self.driver.execute_script(js)
#                     #     time.sleep(0.1)
#                     #     ele = "/html[@id='html']/body[@id='body']/footer[@id='masterFooter']/div[@class='container-xxl']/div[@class='d-flex justify-content-between align-items-baseline py-6']"
#                     #     if self.driver.find_element(By.XPATH, ele):
#                     #         self.driver.find_element(By.XPATH, ele).click()
#                     # # 设置灵活等待，最长等待10s，轮询间隔为1s
#                     # wait = WebDriverWait(self.driver, timeout=3, poll_frequency=1)
#                     # 此处不加休眠时间获取到的html页面不全！！！
#                     time.sleep(3)
#                     page_source = self.driver.page_source
#                     my_page = BeautifulSoup(page_source, 'lxml')
#                     my_page.prettify()
#
#                     tbodys = my_page.find('tbody', class_="align-middle text-nowrap")
#                     if int(count) >= 10:
#                         tbodys = my_page.find('tbody', class_="align-middle text-nowrap paywall-mask")
#                     datasImg2 = []
#                     datasName2 = []
#                     trs2 = tbodys.find_all('tr')
#                     if trs2:
#                         try:
#                             for tr2 in trs2:
#                                 # 获取tokenImgInfo数据
#                                 dataImgdit2 = {}
#                                 address = tr2.find('a')["data-bs-title"]
#                                 img_url = tr2.find('img')["src"].split('?')[0]
#                                 img_name = img_url.split("/")[3].split('?')[0]
#                                 dataImgdit2["token_label"] = labelName
#                                 dataImgdit2["token_address"] = address
#                                 dataImgdit2["token_imgUrl"] = imgUrl + img_url
#                                 dataImgdit2["token_imgName"] = img_name
#                                 dataImgdit2["token_chain"] = 'Ethereum'
#                                 datasImg2.append(dataImgdit2)
#                                 # 获取tokenTag数据
#                                 dataNamedit2 = {}
#                                 token_address = tr2.find('a')["data-bs-title"]
#                                 token_nameTag1 = tr2.find('span', class_="text-truncate").get_text()
#                                 token_nameTag2 = tr2.find('span', class_="text-muted").get_text()
#                                 token_nameTag3 = tr2.find('span', class_="hash-tag text-truncate").get_text()
#                                 dataNamedit2["token_label"] = labelName
#                                 dataNamedit2["token_address"] = token_address
#                                 if token_nameTag1 is not None:
#                                     dataNamedit2["token_nameTag"] = token_nameTag1 + token_nameTag2
#                                 else:
#                                     dataNamedit2["token_nameTag"] = token_nameTag3 + token_nameTag2
#                                 dataNamedit2["token_chain"] = 'Ethereum'
#                                 datasName2.append(dataNamedit2)
#                             df3 = pandas.DataFrame(datasImg2)
#                             df3.to_csv("tokens_imgInfo_ETH.csv", mode='a', header=False, index=False)
#                             df4 = pandas.DataFrame(datasName2)
#                             df4.to_csv("tokens_nameTagInfo_ETH.csv", mode='a', header=False, index=False)
#                             time.sleep(random.random())
#                         except Exception as e:
#                             logging.error("获取token<=100的%s的Img和Name出错%s" % (labelName, e))
#                             errorData = [
#                                 {"labelName": labelName, "token_url": url, "token_sum": int(count), "type": "parser"}]
#                             ef = pandas.DataFrame(errorData)
#                             ef.to_csv("error_tokens_imgInfo_ETH.csv", mode='a', header=False, index=False)
#             except Exception as e:
#                 logging.error("%s获取出现错误:%s" % (labelName, e))
#                 errorData = [{"labelName": labelName, "token_url": url, "token_sum": int(count), "type": "csv"}]
#                 ef = pandas.DataFrame(errorData)
#                 ef.to_csv("error_tokens_imgInfo_ETH.csv", mode='a', header=False, index=False)
#
#     def login(self):
#         ele = "/html[@id='html']/body[@id='body']/main[@id='content']/section[@class='container-xxl pt-5 pb-12']/div[@id='ContentPlaceHolder1_divTokenByLabels']/div[@class='tab-content']/div[@id='tab-0-content']/div[@class='card']/div[@class='table-responsive']/div[@id='table-subcatid-0_wrapper']/div[@class='d-flex flex-wrap align-items-center justify-content-between gap-3 p-4 text-dark']/div[@id='table-subcatid-0_paginate']/ul[@class='pagination pagination-sm mb-0']/li[@id='table-subcatid-0_next']"
#         if self.driver.find_element(By.XPATH,ele):
#             self.driver.find_element(By.XPATH,ele).click()
#
#
#
#
#
# if __name__ == '__main__':
#     ll = test_tokens()
#
#     # # 遍历所有token的URL，下载图片到本地存储
#     # print("开始下载图片："+ time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) +"**********************")
#     # ll.get_token_Img("tokens_imgInfo_ETH.csv")
#     # print("结束下载：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "**********************")
