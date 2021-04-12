from selenium import webdriver
from time import sleep
from PIL import Image, ImageEnhance
import pytesseract

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://admin.tiac.youkehudong.com/")
driver.implicitly_wait(10)
driver.find_element_by_css_selector('[class="loginChange"]').click()
sleep(1)
driver.find_elements_by_css_selector('span > input')[0].send_keys('admin')
driver.find_elements_by_css_selector('span > input')[1].send_keys('a123456')
 # 截图或验证码图片保存地址

# screenImg = "D://a.png'"

# 浏览器页面截屏

driver.get_screenshot_as_file("D://a.png")

# 定位验证码位置及大小

location = driver.find_element_by_id('s-canvas').location

size = driver.find_element_by_id('s-canvas').size

left = location['x']

top = location['y']

right = location['x'] + size['width']

bottom = location['y'] + size['height']

# 从文件读取截图，截取验证码位置再次保存

img = Image.open("D://a.png").crop((left, top, right, bottom))

img = img.convert('L') # 转换模式：L | RGB

img = ImageEnhance.Contrast(img) # 增强对比度

img = img.enhance(2.0) # 增加饱和度

img.save("D://a.png")

# 再次读取识别验证码

img = Image.open("D://a.png")

code = pytesseract.image_to_string(img).replace(' ', '')

# code= pytesser.image_file_to_string(screenImg)

# print(code.strip())
# 输入验证码
driver.find_elements_by_css_selector('span > input')[2].send_keys(code.strip())
driver.find_element_by_css_selector('span > button').click()