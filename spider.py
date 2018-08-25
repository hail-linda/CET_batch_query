# -*- coding: utf-8 -*-
# Author = Linda
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import pandas as pd
import unittest, time, re , os
import argparse , wget
import sys
import os.path
from datetime import datetime
from PIL import Image
import numpy as np
import config , shutil
import tensorflow as tf
from tensorflow.python.platform import gfile
import captcha_model as captcha
import captcha as cap
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

reload(sys)
sys.setdefaultencoding('utf8')

IMAGE_WIDTH = config.IMAGE_WIDTH
IMAGE_HEIGHT = config.IMAGE_HEIGHT

CHAR_SETS = config.CHAR_SETS
CLASSES_NUM = config.CLASSES_NUM
CHARS_NUM = config.CHARS_NUM

FLAGS = None



class CETBatchQuery(unittest.TestCase):
    def setUp(self):
        service_args = []
        service_args.append('--load-images=no')
        service_args.append('--disk-cache=yes')
        service_args.append('--ignore-ssl-errors=true')

	fireFoxOptions = webdriver.FirefoxOptions()
	fireFoxOptions.set_headless()
	
        self.driver = webdriver.Firefox(firefox_options=fireFoxOptions)

        self.driver.implicitly_wait(10)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_CET_batch_query(self):
        csv_1 = pd.read_csv("rsc_1.csv")
        driver = self.driver
        i=0
        print("\n")
        print(time.strftime('%H_%M_%S',time.localtime(time.time())))
        print("\n")
	shutil.rmtree('captcha_dir')
	os.makedirs('captcha_dir')
        while i<csv_1.shape[0]:
		driver.get("http://cet.neea.edu.cn/cet/")
		driver.find_element_by_id("zkzh").click()
		driver.find_element_by_id("zkzh").clear()
                driver.find_element_by_id("zkzh").send_keys(str(csv_1.loc[i,"准考证"]))
		driver.find_element_by_id("name").click()
		driver.find_element_by_id("name").clear()
                driver.find_element_by_id("name").send_keys(csv_1.loc[i,"姓名"].decode("utf-8"))
		for a in range(3):
			driver.find_element_by_id("name").click()		
			driver.find_element_by_id("verify").click()

		dr = driver.find_element_by_id("img_verifys")
		try:
			wget.download(dr.get_attribute('src'))
		except:
			for a in range(4):
				time.sleep(0.02)
				driver.find_element_by_id("name").click()		
				driver.find_element_by_id("verify").click()

			dr = driver.find_element_by_id("img_verifys")
			wget.download(dr.get_attribute('src'))

		pic_name = dr.get_attribute('src')[-36:]
		#print(pic_name)
		shutil.move(pic_name, 'captcha_dir/'+pic_name)
		cap.pre_tensor('captcha_dir/'+pic_name)
		driver.find_element_by_id("verify").click()
        	driver.find_element_by_id("verify").clear()
        	driver.find_element_by_id("verify").send_keys(cap.run_predict())
		driver.find_element_by_id("submitButton").click()
	
            	driver.save_screenshot("screenshot/"+str(csv_1.loc[i,"学号"])+".png")
		time.sleep(0.3)
            	try:
                	score = driver.find_element_by_id('s').get_attribute('textContent')
                	listen = driver.find_element_by_id('l').get_attribute('textContent')
                	read = driver.find_element_by_id('r').get_attribute('textContent')
                	write = driver.find_element_by_id('w').get_attribute('textContent')

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
			#if score != '' :
			i=i+1
			print("i:"+str(i))
			print('\n*********************************\n')
			shutil.move('captcha_dir/'+pic_name,"pic_after_use/"+cap.run_predict()+"_"+str(i))
		        print(i,float(i)/csv_1.shape[0],str(csv_1.loc[i,"准考证"]),score,listen,read,write)
            	except:
			os.remove('captcha_dir/'+pic_name)
			print("i:"+str(i))
        	#csv_1.to_xls('result.xls')



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
