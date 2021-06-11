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


# class baiduTest(unittest.TestCase):
    # global title
    # @classmethod
    # def setUpClass(cls):
        # cls.driver = webdriver.Chrome()
        # cls.driver.get('https://www.baidu.com')
        # cls.driver.maximize_window()
        # print('测试开始')

    # @classmethod
    # def tearDownClass(cls):
        # cls.driver.quit()
        # print("-----------测试结束！结果发送中。。。-----------")


    # def save_img(self, img_name):
    #     self.driver.save_screenshot(f'./img/{img_name}.png')

    # @BeautifulReport.add_test_img('baiduTest_test001Ture')
    # def test001Ture(self):  # admin登录
        # global title
        # title = self.driver.title
        # self.save_img('baiduTest_test001Ture')
        # self.assertTrue(title == '百度一下，你就知道')
        # print('测试1')

    # @BeautifulReport.add_test_img('baiduTest_test002False')
    # def test002False(self):
        # self.save_img('baiduTest_test002False')
        # self.assertTrue(title == '1百度一下，你就知道')
        # print('测试2')

# if __name__ == '__main__':
    # testBeautifulReport("t3.py", "report1", "test")
    # unittest.main()


# from userMysql import userSQL
#
#
# userSQL(
#             sshIP='112.74.105.145',
#             sshPort=26622,
#             sshKeyAddress='D:/rock_工作/Rock_id_rsa_2048',
#             databaseIP='172.24.0.17',
#             databaseName='tiac',
#             databasePwd='ciR7td8kQ',
#             sql="update 'user' set is_delete = 0 where phone = '13211111337';"
#                 # "update 'user' set is_delete = 1 where phone = '13211111336';"
#         )


import mysql.connector
import sshtunnel

with sshtunnel.SSHTunnelForwarder(
        ('112.74.105.145', 26622),
        ssh_username='rock.wu',
        ssh_pkey='D:/rock_工作/Rock_id_rsa_2048',
        ssh_private_key_password='123456',
        # ssh_password='服务器的密码',
        remote_bind_address=('172.24.0.17', 3306),
        local_bind_address=('127.0.0.1', 13306)
) as tunnel:
    conn = mysql.connector.connect(
        user='rock.wu',
        password='ciR7td8kQ',
        host='127.0.0.1',
        port=13306,
        database='tiac',
    )
    cursor = conn.cursor()
    phoneList = [('13211111337'), ('13211111337')]
    # list1 = [1, 2]
    # commit_phoneList = [[list1[i], phoneList[i]] for i in range(len(phoneList))]
    # print(commit_phoneList)

    try:
        sql = "update `user` set is_delete = 1 where phone = %s;"
        print(sql)
        # 使用 execute()  方法执行 SQL 查询
        cursor.executemany(sql, phoneList)
        # 提交到数据库
        conn.commit()
        # 使用 fetchone() 方法获取单条数据.
        # data = cursor.fetchall()
        # print(data)
    except:
        # 发生错误时回滚
        conn.rollback()
    # 关闭数据库连接
    cursor.close()