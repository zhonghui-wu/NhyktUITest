# coding: utf-8
from BeautifulReport import BeautifulReport
from BeautifulReport.BeautifulReport import HTML_IMG_TEMPLATE
from beautifulReport import force_attach_image
from selenium import webdriver
import unittest
import os


# def force_attach_image(img_nm):
#     img_path = os.path.abspath('{}'.format(BeautifulReport.img_path))
#     data = BeautifulReport.img2base(img_path, img_nm + '.png')
#     print(HTML_IMG_TEMPLATE.format(data, data))


class baiduTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get('https://www.baidu.com')
        cls.driver.maximize_window()
        print('test start')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        print('test end')

    def save_img(self, img_name):
        self.driver.save_screenshot(f'./img/{img_name}.png')

    @BeautifulReport.add_test_img('baiduTest_test001Ture')
    def test001Ture(self):
        title = self.driver.title
        self.save_img('baiduTest_test001Ture')
        self.assertTrue(title == '百度一下，你就知道')
        force_attach_image('baiduTest_test001Ture')

    @BeautifulReport.add_test_img('baiduTest_test002False')
    def test002False(self):
        title = self.driver.title
        self.save_img('baiduTest_test002False')
        self.assertTrue(title == '百度一下，你就知道1')


if __name__ == '__main__':
    test_suite = unittest.defaultTestLoader.discover('.', pattern='ddtest.py')
    result = BeautifulReport(test_suite)
    result.report(filename='测试报告', description='测试deafult报告', report_dir='./report', theme='theme_default')
