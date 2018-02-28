# -*- coding: utf-8 -*-
# Author = Linda
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import pandas as pd
import numpy as np
import unittest, time, re

class CETBatchQuery(unittest.TestCase):
    def setUp(self):
        service_args = []
        service_args.append('--load-images=no')
        service_args.append('--disk-cache=yes')
        service_args.append('--ignore-ssl-errors=true')

        self.driver = webdriver.PhantomJS(service_args=service_args)
        self.driver.implicitly_wait(10)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_CET_batch_query(self):
        csv_1 = pd.read_csv("rsc_1.csv")
        driver = self.driver
        i=1
        print("\n")
        print(time.strftime('%H_%M_%S',time.localtime(time.time())))
        print("\n")

        while i<csv_1.shape[0]:
            driver.get("http://www.chsi.com.cn/cet/")
            driver.find_element_by_id("zkzh").click()
            driver.find_element_by_id("zkzh").clear()
            driver.find_element_by_id("zkzh").send_keys(str(csv_1.loc[i,"准考证号"]))
            driver.find_element_by_id("xm").click()
            driver.find_element_by_id("xm").clear()
            driver.find_element_by_id("xm").send_keys(csv_1.loc[i,"姓名"].decode("utf-8"))
            driver.find_element_by_id("submitCET").click()
            source = driver.page_source
            driver.set_window_size(1920,1080)
            driver.save_screenshot(str(csv_1.loc[i,"学号"])+".png")

            try:
                score = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/table/tbody/tr[6]/td/span').get_attribute('textContent')
                listen = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/table/tbody/tr[7]/td[2]').get_attribute('textContent')
                read = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/table/tbody/tr[8]/td[2]').get_attribute('textContent')
                write = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/table/tbody/tr[9]/td[2]').get_attribute('textContent')

                score = str(re.findall(r'\d+', score, flags=0))
                listen = str(re.findall(r'\d+', listen, flags=0))
                read = str(re.findall(r'\d+', read, flags=0))
                write = str(re.findall(r'\d+', write, flags=0))

                score = score[3:-2]
                listen = listen[3:-2]
                read = read[3:-2]
                write = write[3:-2]

                csv_1.loc[i, "总成绩"] = score
                csv_1.loc[i, "听力"] = listen
                csv_1.loc[i, "阅读"] = read
                csv_1.loc[i, "写作与翻译"] = write

                csv_1.to_csv("rsc_1.csv")

                print(i,float(i)/csv_1.shape[0],str(csv_1.loc[i,"准考证号"]),score,listen,read,write)
            except:
                print("ERROR")
            i=i+1
        csv_1.to_xls('result.xls')



    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
