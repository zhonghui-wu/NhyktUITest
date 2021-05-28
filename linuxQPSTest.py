from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('blink-settings=imagesEnabled=false')
chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(chrome_options=chrome_options)

list={'http://192.168.247.128:4444/wd/hub': 'chrome'
      }
for host, browser in list.items():
    chrome_capabilities = {
        "browserName": browser,  # 浏览器名称
        "browserVersion": 90.0,
        "version": "",  # 操作系统版本
        "platform": "windows",  # 平台，这里可以是windows、linux、andriod等等
        "javascriptEnabled": True  # 是否启用js
    }
    driver = webdriver.Remote(options=chrome_options,command_executor=host, desired_capabilities=chrome_capabilities)
    driver.get("http://yk.callwine.net/sem-portal/auth/toBoxLiveCourses.do?adslNum=10077")
    # print('dakai')
    for i in range(30):

        all = driver.current_window_handle
        # 新标签页打开
        driver.execute_script('window.open("http://yk.callwine.net/sem-portal/auth/toBoxLiveCourses.do?adslNum=10077")')
        # print('1')
        if len(all) == 120:
            print('end')