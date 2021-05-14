import time, unittest
import HTMLTestRunner
import zmail
from BeautifulReport import BeautifulReport

from TestRunner import createTestRunner
from sendEmail import sEmail


class a(unittest.TestCase):
    def test001b(self):
        pass

    def test002c(self):
        pass

    def test003d(self):
        pass


if __name__ == '__main__':
    createTestRunner('.', 't4.py', './report.html', '南海云课堂管理后台自动化测试报告', '南海云课堂管理后台主要流程测试')
    time.sleep(1)
    sEmail('./report.html', '1483836794@qq.com')