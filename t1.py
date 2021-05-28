import threading,unittest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep


class ykzb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('blink-settings=imagesEnabled=false')
        chrome_options.add_argument('--disable-gpu')
        chrome_capabilities = {
            "browserName": 'chrome',  #
            "platform": "Linux",  #
            "javascriptEnabled": True  #
        }
        cls.driver = webdriver.Remote(options=chrome_options, command_executor='http://192.168.5.233:4444/wd/hub',
                                  desired_capabilities=chrome_capabilities)


    @classmethod
    def tearDownClass(cls):
        print("-----------测试结束！-----------")


    def execute_func(self):
        for i in range(10):
            self.driver.get('http://yk.callwine.net/sem-portal/auth/toBoxLiveCourses.do?adslNum=10077')
            self.driver.execute_script(
                'window.open("http://yk.callwine.net/sem-portal/auth/toBoxLiveCourses.do?adslNum=10077")')
            all = self.driver.window_handles
            print(len(all))


    def test1_many_thread(self):
        start = datetime.now()
        threads = []
        for _ in range(2):  # 循环创建500个线程
            t = threading.Thread(target=self.execute_func())
            threads.append(t)

        for t in threads:  # 循环启动500个线程
            t.start()
            t.join()

        duration = datetime.now() - start
        print(duration)


if __name__ == '__main__':
    unittest.main()