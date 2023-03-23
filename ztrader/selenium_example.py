import time

from selenium import webdriver
from selenium.webdriver.common.by import By


opt = webdriver.ChromeOptions()
opt.headless = True

driver = webdriver.Chrome(options=opt)

# driver.get('https://www.baidu.com')

# print(driver.current_window_handle)
# print(driver.page_source)
# # 在百度搜索框中搜索 'python'
# ele = driver.find_element('id','su').get_attribute('value')

driver.get('http://quote.eastmoney.com/sh601238.html')
for i in range(10):
    ele = driver.find_element(By.CLASS_NAME, "blinkred")
# driver.find_element('xpath', "//div[@class='btn self-btn bg s_btn']")

    print(ele.text)
# # 点击 "百度搜索"
# driver.find_element('id', 'su').click()

# time.sleep(6)
# # 退出浏览器
# driver.quit()


EXCHANGE_NAME={
    'sz':['000', '002', '003'],
    'sh':['600', '601', '603','605']
}

def exchange_mapping(sid):
    head = sid[0:3]
    if head in EXCHANGE_NAME['sz']:
        return 'sz'
    if head in EXCHANGE_NAME['sh']:
        return 'sh'
    else:
        return None


HTML_BASE='http://quote.eastmoney.com/'
HTML_SID = HTML_BASE+exchange_mapping(sid)+sid
