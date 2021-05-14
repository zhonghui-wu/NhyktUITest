from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

start = time.time()
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('blink-settings=imagesEnabled=false')
chrome_options.add_argument('--disable-gpu')
list={'http://192.168.0.218:4000/wd/hub': 'chrome'
      }
for host, browser in list.items():
    # chrome_capabilities = {
    #     "browserName": browser,  # 浏览器名称
    #     "browserVersion": 90.0,
    #     "version": "6.1",  # 操作系统版本
    #     "platform": "windows 7",  # 平台，这里可以是windows、linux、andriod等等
    #     "javascriptEnabled": True  # 是否启用js
    # }
    driver = webdriver.Remote(options=chrome_options, command_executor=host)#, desired_capabilities=chrome_capabilities)
    driver.get("http://yk.callwine.net/sem-portal/auth/toBoxLiveCourses.do?adslNum=10067")
    driver.implicitly_wait(5)
    driver.switch_to.frame('right')
    driver.find_element_by_id("video_container").click()
    for i in range(100):

        all =driver.window_handles
        # 新标签页打开
        driver.execute_script('window.open("http://yk.callwine.net/sem-portal/auth/toBoxLiveCourses.do?adslNum=10067")')
        driver.find_element_by_id("video_container").click()
        title = driver.title
        if title != '课堂详情':
            print('打开页面失败')

        if len(all) == 100:
            end = time.time()
            print('open 101 succeed! use time : %s Seconds' % (end - start))
            # driver.quit()