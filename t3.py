import os, time, pytesseract, stat
import traceback
import unittest
from BeautifulReport import BeautifulReport
from selenium import webdriver
from beautifulReport import testBeautifulReport
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageEnhance
from config import imgFile
from selenium.webdriver.common.keys import Keys


class baiduTest(unittest.TestCase):
    global title
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get('https://www.baidu.com')
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        print("-----------测试结束！结果发送中。。。-----------")


    def save_img(self, img_name):
        self.driver.save_screenshot(f'./img/{img_name}.png')

    @BeautifulReport.add_test_img('baiduTest_test001Ture')
    def test001Ture(self):  # admin登录
        global title
        title = self.driver.title
        self.save_img('baiduTest_test001Ture')
        self.assertTrue(title == '百度一下，你就知道')

    @BeautifulReport.add_test_img('baiduTest_test002False')
    def test002False(self):
        self.save_img('baiduTest_test002False')
        self.assertTrue(title == '1百度一下，你就知道')


if __name__ == '__main__':
    testBeautifulReport("t3.py", "report1", "test")
