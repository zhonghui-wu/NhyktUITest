import HTMLTestRunner
import unittest


def createTestRunner(testCasePath, testCase, reportPath, reportTitle, testCaseMsg):

    # 测试用例保存的目录
    case_dirs = testCasePath
    # 加载测试用例
    discover = unittest.defaultTestLoader.discover(case_dirs, testCase)
    # 运行测试用例同时保存测试报告
    test_report_path = reportPath
    with open(test_report_path, "wb") as report_file:
        runner = HTMLTestRunner.HTMLTestRunner(stream=report_file, title=reportTitle, description=testCaseMsg)
        runner.run(discover)

    return