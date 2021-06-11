import unittest
from unittestreport import TestRunner


def createTestRunner(testClass, reportName, report_dir, title, tester, objectName):
    '''

    :param testClass: 测试类的名字
    :param reportName: 测试报告名称.html
    :param report_dir: 测试报告地址
    :param title: 测试报告标题
    :param tester: 测试人员
    :param objectName: 项目名称 + 测试用例
    :return:
    '''
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testClass)
    runner = TestRunner(
        suite=suite,
        filename=reportName,
        report_dir=report_dir,
        title=title,
        tester=tester,
        desc=objectName
    )
    # count：用来指定用例失败重运行的次数
    # interval：指定每次重运行的时间间隔
    runner.rerun_run(count=3, interval=2)

    return