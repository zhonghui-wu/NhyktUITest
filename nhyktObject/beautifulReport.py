import unittest
from BeautifulReport import BeautifulReport


def testBeautifulReport(testCase, reportTitle, testMsg):  # 无法发送到邮件

    suite_tests = unittest.defaultTestLoader.discover(".", pattern=testCase, top_level_dir=None)
    BeautifulReport(suite_tests).report(filename=reportTitle, description=testMsg, log_path='.')

    return