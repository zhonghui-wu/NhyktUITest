from selenium import webdriver
from time import sleep
from PIL import Image, ImageEnhance
import pytesseract, unittest, time
from selenium.webdriver.common.keys import Keys


class NhyktTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("https://admin.tiac.youkehudong.com/")
        cls.driver.implicitly_wait(3)
        cls.driver.find_element_by_css_selector('[class="loginChange"]').click()

    @classmethod
    def tearDownClass(cls):
        print("-----------测试结束！结果发送中。。。-----------")

    def GetCode(self):

        # 浏览器页面截屏
        self.driver.get_screenshot_as_file("D://a.png")

        # 定位验证码位置及大小
        location = self.driver.find_element_by_id('s-canvas').location

        size = self.driver.find_element_by_id('s-canvas').size

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        # 从文件读取截图，截取验证码位置再次保存
        img = Image.open("D://a.png").crop((left, top, right, bottom))

        img = img.convert('L')  # 转换模式：L | RGB

        img = ImageEnhance.Contrast(img)  # 增强对比度

        img = img.enhance(2.0)  # 增加饱和度

        img.save("D://a.png")

        # 再次读取识别验证码
        img = Image.open("D://a.png")

        code = pytesseract.image_to_string(img).replace(' ', '')
        # code= pytesser.image_file_to_string(screenImg)
        return code.strip()

    def test1Login(self):
        sleep(1)
        self.driver.find_elements_by_css_selector('span > input')[0].send_keys('admin')
        self.driver.find_elements_by_css_selector('span > input')[1].send_keys('a123456')
        code = self.GetCode()
        # 输入验证码
        self.driver.find_elements_by_css_selector('span > input')[2].send_keys(code)
        self.driver.find_element_by_css_selector('span > button').click()

        while True:
            # 判断是否有这个元素
            try:
                warn = self.driver.find_element_by_css_selector('[class="ant-form-explain"]')
            except:
                break
            if warn:
                self.driver.find_element_by_id('s-canvas').click()
                code = self.GetCode()
                inp = self.driver.find_elements_by_css_selector('span > input')[2]
                # 清除输入框内容
                inp.send_keys(Keys.CONTROL+'a')
                inp.send_keys(Keys.DELETE)
                # 输入验证码
                inp.send_keys(code)
                self.driver.find_element_by_css_selector('span > button').click()
                # print(warn.text)

            else:
                break

        return print('登录成功')

    def test2AddCourse(self):
        self.driver.find_element_by_xpath('//*[@id="menu"]/li[5]/div').click()
        self.driver.find_element_by_xpath('//*[@id="menu"]/li[5]/ul/li[1]').click()
        self.driver.find_element_by_css_selector('[class=" ant-tabs-tab"]').click()
        sleep(1)
        self.driver.find_element_by_css_selector('div.subjectManagement > button').click()
        # 增加学科
        self.driver.find_element_by_css_selector('span > input').send_keys('测试')
        sleep(1)
        self.driver.find_element_by_xpath('//*[@class="ant-modal-footer"]/div/button[2]').click()
        # 下面删除学科
        # 将屏幕滚动到最下面
        self.driver.execute_script("var q=document.documentElement.scrollTop=10000")
        # 点击输入页数
        self.driver.find_elements_by_xpath('//*[@class="ant-pagination-options-quick-jumper"]/input')[1].send_keys('100000\n')
        all = self.driver.find_elements_by_xpath('//*[@class="subjectManagement"]/div//table/tbody/tr/td[2]')
        for i in all:
            print(i)
            # if "测试" in course.text:
            #     print('课程添加成功')


if __name__ == '__main__':
    unittest.main()