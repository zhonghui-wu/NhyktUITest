import HTMLTestRunner

from selenium import webdriver
from time import sleep
from PIL import Image, ImageEnhance
import pytesseract, unittest, time
from selenium.webdriver.common.keys import Keys
import win32com.client  # 上传文件模块
from TestRunner import createTestRunner
from sendEmail import sEmail


class NhyktTest(unittest.TestCase):
    global timelast, Phone, courseName

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("https://admin.tiac.youkehudong.com/")
        cls.driver.implicitly_wait(5)
        cls.driver.find_element_by_css_selector('[class="loginChange"]').click()

    @classmethod
    def tearDownClass(cls):
        print("-----------测试结束！结果发送中。。。-----------")

    def GetCode(self):  # 获取图片验证码

        # 浏览器页面截屏
        self.driver.get_screenshot_as_file(r"D:\\a.png")

        # 定位验证码位置及大小
        location = self.driver.find_element_by_id('s-canvas').location

        size = self.driver.find_element_by_id('s-canvas').size

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        # 从文件读取截图，截取验证码位置再次保存
        img = Image.open(r"D:\\a.png").crop((left, top, right, bottom))

        img = img.convert('L')  # 转换模式：L | RGB

        img = ImageEnhance.Contrast(img)  # 增强对比度

        img = img.enhance(2.0)  # 增加饱和度

        img.save(r"D:\\a.png")

        # 再次读取识别验证码
        img = Image.open(r"D:\\a.png")

        code = pytesseract.image_to_string(img).replace(' ', '')
        # code= pytesser.image_file_to_string(screenImg)
        return code.strip()

    def test001AdminLogin(self):  # admin登录
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
                inp.send_keys(Keys.CONTROL + 'a')
                inp.send_keys(Keys.DELETE)
                # 输入验证码
                inp.send_keys(code)
                self.driver.find_element_by_css_selector('span > button').click()
                # print(warn.text)

            else:
                break

        return print('登录成功')

    def test002AddCourse(self):  # 新增学科
        self.driver.find_element_by_xpath('//*[@id="menu"]/li[5]/div').click()
        self.driver.find_element_by_xpath('//*[@id="menu"]/li[5]/ul/li[1]').click()
        self.driver.find_element_by_css_selector('[class=" ant-tabs-tab"]').click()
        # 增加学科
        sleep(1)
        self.driver.find_element_by_css_selector('div.subjectManagement > button').click()
        self.driver.find_element_by_css_selector('span > input').send_keys('rock测试')
        sleep(1)
        self.driver.find_element_by_xpath('//*[@class="ant-modal-footer"]/div/button[2]').click()
        # 将屏幕滚动到最下面
        self.driver.execute_script("var q=document.documentElement.scrollTop=10000")
        # 点击输入页数，进入最后一页
        self.driver.find_elements_by_xpath('//*[@class="ant-pagination-options-quick-jumper"]/input')[1].send_keys(
            '100000\n')
        sleep(1)
        all = self.driver.find_elements_by_xpath('//*[@class="subjectManagement"]/div//table/tbody/tr')
        for i in all:
            if "rock测试" in i.text:
                print('学科添加成功')
                deletes = i.find_elements_by_xpath('//*[@class="subjectManagement"]/div//table/tbody/tr/td/a[2]')
                msg = len(deletes)
                deletes[msg - 1].click()
                sleep(1)
                self.driver.find_element_by_css_selector(
                    'div.ant-modal-confirm-btns > button.ant-btn.ant-btn-primary').click()
        return print("学科新增功能测试正常")

    def test003AddSchool(self):  # 新增学校
        self.driver.find_element_by_css_selector('[class=" ant-tabs-tab"]').click()
        sleep(1)
        self.driver.find_elements_by_css_selector('[class="ant-btn ant-btn-primary"]')[0].click()
        # 新增信息信息填写
        schoolForm = self.driver.find_elements_by_css_selector('[class="ant-input"]')
        # 学校名称
        sleep(1)
        schoolForm[0].send_keys('rock测试学校')
        # 学校简称
        schoolForm[1].send_keys('测试')
        # 学校标识码
        schoolForm[2].send_keys('1')
        # 学校类型
        self.driver.find_elements_by_css_selector('[class="select_option ant-select ant-select-enabled"]')[0].click()
        # 这里选的是第一个类型
        self.driver.find_elements_by_css_selector('[class="ant-select-dropdown-menu-item"]')[0].click()
        self.driver.find_element_by_xpath('//*[@class="ant-modal-footer"]/div/button[2]').click()
        # 获取第一页的学校列表
        sleep(1)
        schools = self.driver.find_elements_by_css_selector('[class="ant-table-row ant-table-row-level-0"]')
        for school in schools:
            if 'rock测试学校' in school.text:
                schools[0].find_element_by_css_selector('[class="option-danger-color"]').click()
                sleep(1)
                self.driver.find_element_by_css_selector(
                    ' div.ant-modal-confirm-btns > button.ant-btn.ant-btn-primary').click()
        return print('学校新增功能测试正常')

    def test004AddTeacher(self):  # 新增老师
        global newTeacherPhone, Phone
        self.driver.find_element_by_xpath('//*[@id="menu"]/li[4]/div').click()
        self.driver.find_element_by_xpath('//*[@id="menu"]/li[4]/ul/li[1]').click()
        # 点击新增老师按钮
        self.driver.find_element_by_xpath('//*[@class="option_group"]/button[1]').click()
        # 老师信息表单
        sleep(1)
        teacherFrom = self.driver.find_elements_by_css_selector('[class="ant-input"]')
        # 老师姓名
        teacherFrom[0].send_keys('rock测试')
        # 老师手机号
        Phone = 11111157
        teacherFrom[1].send_keys('131' + str(Phone))
        # 老师教龄
        teacherFrom[5].send_keys('1')
        # 选择老师生日
        self.driver.find_element_by_css_selector('[class="ant-calendar-picker-input ant-input"]').click()
        self.driver.find_elements_by_css_selector('[class="ant-calendar-date"]')[0].click()
        # 将屏幕滚动到最下面
        self.driver.execute_script("var q=document.documentElement.scrollTop=10000")
        # 选择所属学校
        self.driver.find_elements_by_css_selector('[class="ant-select-selection__placeholder"]')[1].click()
        self.driver.find_elements_by_css_selector('[class="ant-select-dropdown-menu-item"]')[0].click()
        # 选择学科
        self.driver.find_elements_by_css_selector('[class="ant-select-selection__placeholder"]')[2].click()
        self.driver.find_element_by_css_selector('li.ant-select-dropdown-menu-item.ant-select-dropdown-menu-item-active').click()
        # 选择教学年级
        self.driver.find_element_by_css_selector('[class="ant-tag"]').click()
        sleep(1)
        self.driver.find_elements_by_css_selector('[class="input-radio"]')[0].click()
        self.driver.find_element_by_css_selector('[class="ant-btn ant-btn-primary"]').click()
        # 提交
        self.driver.find_element_by_css_selector('[class="addbtn ant-btn ant-btn-primary"]').click()
        while True:
            ele = self.driver.find_elements_by_css_selector('[class="title_bar"]')
            if ele:
                # 滑到顶部
                self.driver.execute_script("var q=document.documentElement.scrollTop=0")
                Phone +=1
                # 清除输入框内容
                teacherFrom[1].send_keys(Keys.CONTROL + 'a')
                teacherFrom[1].send_keys(Keys.DELETE)
                # 重新输入
                newTeacherPhone = '131' + str(Phone)
                teacherFrom[1].send_keys(newTeacherPhone)
                # 将屏幕滚动到最下面
                self.driver.execute_script("var q=document.documentElement.scrollTop=10000")
                # 提交
                self.driver.find_element_by_css_selector('[class="addbtn ant-btn ant-btn-primary"]').click()
                sleep(1)
            else:
                break
        # 获取老师列表
        teacherListPhone = self.driver.find_elements_by_xpath('//*[@class="ant-table-tbody"]/tr/td')[3]
        if newTeacherPhone in teacherListPhone.text:
            print('新增老师成功')
        else:
            print('新增失败')
        return print('新增老师功能测试正常')

    def test005AddStudent(self):  # 新增学生
        global newStudentPhone, Phone
        self.driver.find_element_by_xpath('//*[@id="menu"]/li[4]/ul/li[2]').click()
        sleep(1)
        self.driver.find_element_by_xpath('//*[@class="option_group"]/button[1]').click()
        # 填写学生基本信息
        sleep(1)
        studentFrom = self.driver.find_elements_by_css_selector('[class="ant-input"]')
        # 输入学生姓名
        studentFrom[0].send_keys('rock测试')
        # 输入学生家长手机号
        studentFrom[1].send_keys('132' + str(Phone))
        # 选择生日
        self.driver.find_element_by_css_selector('[class="ant-calendar-picker-input ant-input"]').click()
        self.driver.find_elements_by_css_selector('[class="ant-calendar-date"]')[0].click()
        # 选择学校
        self.driver.find_elements_by_css_selector('[class="ant-select-selection__placeholder"]')[0].click()
        self.driver.find_elements_by_css_selector('[class="ant-select-dropdown-menu-item"]')[0].click()
        # 选择年级
        self.driver.find_elements_by_css_selector('[class="ant-select-selection__placeholder"]')[1].click()
        self.driver.find_element_by_css_selector('li.ant-select-dropdown-menu-item.ant-select-dropdown-menu-item-active').click()
        # 点击提交
        self.driver.find_element_by_css_selector('[class="addbtn ant-btn ant-btn-primary"]').click()
        while True:
            ele = self.driver.find_elements_by_css_selector('[class="title_bar"]')
            if ele:
                Phone += 1
                # 清除输入框内容
                studentFrom[1].send_keys(Keys.CONTROL + 'a')
                studentFrom[1].send_keys(Keys.DELETE)
                # 重新输入
                newStudentPhone = '132' + str(Phone)
                studentFrom[1].send_keys(newStudentPhone)
                # 提交
                try:
                    self.driver.find_element_by_css_selector('[class="addbtn ant-btn ant-btn-primary"]').click()
                except:
                    pass
                sleep(1)
            else:
                break
        # 获取老师列表
        teacherListPhone = self.driver.find_elements_by_xpath('//*[@class="ant-table-tbody"]/tr/td')[3]
        if newStudentPhone in teacherListPhone.text:
            print('新增学生成功')
        else:
            print('新增学生失败')
        return print('新增学生功能测试正常')

    def test006AddTourclass(self): # 新增巡课
        global timelast
        self.driver.find_element_by_xpath('//*[@id="menu"]/li[4]/ul/li[3]').click()
        sleep(1)
        self.driver.find_element_by_xpath('//*[@class="option_group"]/button[1]').click()
        # 填写巡课信息
        timelast = int(time.time()*10000) % 10000 # 获取时间戳最后几位
        auditName = 'rock巡课' + str(timelast)
        self.driver.find_elements_by_css_selector('[class="ant-input"]')[0].send_keys(auditName)
        # 生日
        self.driver.find_element_by_css_selector('[class="ant-calendar-picker-input ant-input"]').click()
        self.driver.find_elements_by_css_selector('[class="ant-calendar-date"]')[0].click()
        # 所属学校
        self.driver.find_elements_by_css_selector('[class="ant-select-selection__placeholder"]')[0].click()
        self.driver.find_elements_by_css_selector('[class="ant-select-dropdown-menu-item"]')[0].click()
        # 提交
        self.driver.find_element_by_css_selector('[class="addbtn ant-btn ant-btn-primary"]').click()
        # 获取巡课列表
        auditList = self.driver.find_elements_by_xpath('//*[@class="ant-table-tbody"]/tr/td')[2]
        if auditName in auditList.text:
            print('新增巡课成功')
        else:
            print('新增巡课失败')
        return print('新增巡课功能测试正常')

    def test007AddLiveCourse(self):  # 新增直播课
        global courseName
        self.driver.find_element_by_xpath('//*[@id="menu"]/li[2]/div').click()
        self.driver.find_element_by_xpath('//*[@id="menu"]/li[2]/ul/li[3]').click()
        sleep(1)
        self.driver.find_element_by_xpath('//*[@class="button_group"]/button[1]').click()
        # 输入课程名称
        timelast = int(time.time() * 10000) % 10000
        courseName = 'rock课程' + str(timelast)
        sleep(1)
        self.driver.find_element_by_css_selector('[class="ant-input"]').send_keys(courseName)
        # 点击上传封面
        self.driver.find_element_by_css_selector('[class="ant-upload"]').click()
        sh = win32com.client.Dispatch("WScript.shell")
        sleep(1)
        sh.Sendkeys('D:\\a.png\n')  # \n == 回车
        sleep(1)
        self.driver.find_element_by_css_selector('[class="ant-btn ant-btn-primary"]').click()
        # 选择学科
        sleep(1)
        self.driver.find_element_by_css_selector('[class="ant-select-selection__rendered"]').click()
        self.driver.find_element_by_css_selector(
            '[class="ant-select-dropdown-menu-item ant-select-dropdown-menu-item-active"]').click()
        # 选择上课年级
        self.driver.find_element_by_css_selector('[class="ant-tag"]').click()
        sleep(1)
        self.driver.find_elements_by_css_selector('[class="input-radio"]')[6].click()
        self.driver.find_elements_by_css_selector('[class="ant-btn ant-btn-primary"]')[1].click()
        # 输入课程简介
        self.driver.switch_to.frame('ueditor_1')
        self.driver.find_elements_by_css_selector('[class="view"]')[1].send_keys('测试课程简介')
        # 回到之前的iframe
        self.driver.switch_to.default_content()
        # 点击提交
        sleep(1)
        self.driver.find_element_by_css_selector('[class="addbtn ant-btn ant-btn-primary"]').click()
        # 获取温馨提示弹窗
        warning = self.driver.find_element_by_css_selector('[class="ant-modal-confirm-content"]').text
        if warning:
            print('课程新增成功')
            print('课程管理测试成功')
        else:
            print('课程新增不成功')
        # 点击以后再说
        self.driver.find_elements_by_css_selector('[class="ant-btn"]')[1].click()
        self.driver.find_element_by_xpath('//*[@id="menu"]/li[2]/ul/li[3]').click()
        # 选择去查看
        sleep(1)
        self.driver.find_element_by_css_selector(' tr:nth-child(1) > td:nth-child(9) > a:nth-child(1)').click()
        # 滑到页面最下面点击去排课
        self.driver.execute_script("var q=document.documentElement.scrollTop=10000")
        sleep(1)
        self.driver.find_element_by_css_selector('[class="ant-btn ant-btn-primary"]').click()
        return courseName

    def test008CreateLive(self):  # 排课
        # 进入快速排课,输入上课老师
        self.driver.find_element_by_css_selector('[class="ant-select ant-select-enabled ant-select-no-arrow"]').click()
        self.driver.find_elements_by_css_selector('[class="ant-select-search__field"]')[1].send_keys('rock')
        sleep(1)
        self.driver.find_element_by_css_selector('[class="title"]').click()

        # 选择开课日期为今天
        sleep(1)
        self.driver.find_element_by_css_selector('[class="ant-calendar-picker"]').click()
        sleep(1)
        self.driver.find_element_by_css_selector('[class="ant-calendar-today-btn "]').click()
        # 选择开课时间
        nowTime = time.strftime('%H%M', time.localtime(time.time()))
        sleep(1)
        self.driver.find_elements_by_css_selector('[class="ant-time-picker-input"]')[0].click()
        allHour = self.driver.find_elements_by_xpath('//*[@class="ant-time-picker-panel-select"][1]/ul/li')
        allMinute = self.driver.find_elements_by_xpath('//*[@class="ant-time-picker-panel-select"][2]/ul/li')
        browserHour = self.driver.find_elements_by_css_selector('[class="ant-time-picker-panel-select-option-selected"]')[0]
        browserMinute = self.driver.find_elements_by_css_selector('[class="ant-time-picker-panel-select-option-selected"]')[1]
        nowMinute = nowTime[2] + nowTime[3]
        nowHour = nowTime[0] + nowTime[1]
        if int(nowMinute) > 59:
            subscript1 = int(browserHour.text)+1  # 下标
            allHour[subscript1].click()
        else:
            subscript2 = int(browserMinute.text)+2
            allMinute[subscript2].click()

        self.driver.find_elements_by_css_selector('[class="ant-time-picker-input"]')[1].click()
        etime = str(int(nowHour)+1)+':'+str(nowMinute)
        sleep(1)
        self.driver.find_element_by_css_selector('[class="ant-time-picker-panel-input "]').send_keys(etime)
        self.driver.find_element_by_css_selector('[class="title"]').click()
        # 输入直播名称
        self.driver.find_elements_by_css_selector('[class="ant-input"]')[0].send_keys('rock测试直播')
        self.driver.execute_script("var q=document.documentElement.scrollTop=10000")
        # 点击提交
        self.driver.find_element_by_css_selector('[class="addForm ant-btn ant-btn-primary"]').click()
        liveCourse = self.driver.find_element_by_css_selector(' tr:nth-child(1) > td:nth-child(7)')
        if courseName == liveCourse.text:
            print('排课成功')
        return print('排课管理测试成功')

    def test009TeacherLogin(self):  # 老师登录
        self.driver.execute_script('window.open("https://admin.tiac.youkehudong.com")')
        allHandles = self.driver.window_handles
        self.driver.switch_to.window(allHandles[-1])
        self.driver.find_element_by_css_selector('[class="loginChange"]').click()
        sleep(1)
        self.driver.find_elements_by_css_selector('span > input')[0].send_keys('T2010030489953')
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
                inp.send_keys(Keys.CONTROL + 'a')
                inp.send_keys(Keys.DELETE)
                # 输入验证码
                inp.send_keys(code)
                self.driver.find_element_by_css_selector('span > button').click()

            else:
                break
        ele = self.driver.find_element_by_css_selector('[title="rock"]')
        if ele:
            pass
        else:
            print('未登录')
        return print('老师登录成功')

    def test010TeacherLive(self):  # 老师开始直播
        course = self.driver.find_element_by_css_selector(' tr:nth-child(1) > td:nth-child(5)').text
        # 点击进入直播
        self.driver.find_element_by_css_selector(' tr:nth-child(1) > td:nth-child(9) > span:nth-child(2) > a').click()
        # 获取所有句柄
        sleep(1)
        allHandles = self.driver.window_handles
        # 切换到最后一个句柄
        self.driver.switch_to.window(allHandles[-1])
        # 点击 三次下一步
        self.driver.find_elements_by_css_selector('[class="tic-btn ing"]')[0].click()
        self.driver.find_elements_by_css_selector('[class="tic-btn ing"]')[1].click()
        self.driver.find_elements_by_css_selector('[class="tic-btn ing"]')[1].click()
        # 点击 进入课堂
        self.driver.find_elements_by_css_selector('[class="tic-btn ing"]')[1].click()
        # 点击 上课
        self.driver.find_elements_by_css_selector('[class="tic-btn headerbtn start"]')[0].click()
        # 判断是否上课
        sleep(1)
        ele = self.driver.find_element_by_css_selector('[class="left-time menu-course__time"]')
        if ele:
            print(course + '上课成功')
        else:
            print('未上课')
        return print('老师直播测试成功')

    def test011StudentLogin(self):  # 学生登录
        self.driver.execute_script('window.open("https://student.tiac.ykhdedu.com/login")')
        sleep(1)
        allHandles = self.driver.window_handles
        self.driver.switch_to.window(allHandles[-1])
        self.driver.find_element_by_css_selector('[class="blue_color"]').click()
        sleep(1)
        self.driver.find_elements_by_css_selector('span > input')[0].send_keys('S1992071833190')
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
                inp.send_keys(Keys.CONTROL + 'a')
                inp.send_keys(Keys.DELETE)
                # 输入验证码
                inp.send_keys(code)
                self.driver.find_element_by_css_selector('span > button').click()

            else:
                break

        studentName = self.driver.find_element_by_css_selector('[class="username"]').text
        if studentName:
            print('学生登录成功')

        return

    def test012StudentIntoLive(self):  # 学生进入直播
        # 点击进入直播
        self.driver.find_element_by_xpath('//*[@class="option_item online"]/span').click()
        sleep(2)
        allHandles = self.driver.window_handles
        self.driver.switch_to.window(allHandles[-1])
        sleep(2)
        ele = self.driver.find_element_by_css_selector('[class="left-time menu-course__time"]')
        if ele:
            print('学生进入直播间成功')

        self.driver.switch_to.window(allHandles[2])
        # 老师关闭直播
        self.driver.find_element_by_css_selector('[class="tic-btn headerbtn end red"]').click()
        self.driver.find_element_by_css_selector('[class="ivu-btn ivu-btn-primary ivu-btn-large"]').click()
        # 退出浏览器
        sleep(1)
        self.driver.quit()
        return print('学生进入直播间测试正常,直播间已关闭。')


if __name__ == '__main__':
    createTestRunner('.', 'nhykt.py', './report.html', '南海云课堂管理后台自动化测试报告', '南海云课堂管理后台主要流程测试')
    sleep(1)
    sEmail('./report.html', '1483836794@qq.com')
