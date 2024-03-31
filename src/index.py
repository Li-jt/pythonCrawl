import asyncio
import os
import configparser
import utils.glo as gl

import wx
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from wx.lib.pubsub import pub

from utils.index import get_root_path, address_conversion, name_processing
from utils.requests.index import get_img

chrome_options = Options()
chrome_options.add_argument("--headless")

nodes = {
    1: '.cDZIoX', 2: 'section ul.hdRpMN', 3: '.cDZIoX'
}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(get_root_path(), 'config.ini')

config = configparser.ConfigParser()
config.read(config_path, encoding='utf-8')

# searchMethod = int(input('搜索方式(1:画师id;2:搜索;)：'))
searchMethod = ''

# username = input('作品或用户id：')
username = ''
ageType = 2
page = 1


# if searchMethod == 2:
# ageType = int(input('类型（1:全部，2:全年龄，3:R-18）：'))
def get_data(search, user, type):
    global searchMethod
    global username
    global ageType
    searchMethod = search
    username = user
    ageType = type

    account = config.get('pixiv', 'account')
    password = config.get('pixiv', 'password')

    session = config.get('HttpSession', 'session')

    # driver = webdriver.Chrome()
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 1080 * 2)
    gl.set_value('btn_text', '正在打开pixiv')
    wx.CallAfter(pub.sendMessage, "update")
    driver.get("https://www.pixiv.net/")
    driver.implicitly_wait(20)

    if session:
        driver.add_cookie({
            'name': 'PHPSESSID',
            'value': session,
            'domain': '.pixiv.net'
        })
        driver.refresh()
    else:
        driver.find_element(By.CSS_SELECTOR, '.signup-form')
        driver.find_element(By.CSS_SELECTOR, '.signup-form__submit--login').click()
        driver.find_element(By.CSS_SELECTOR, '.brNKPG')
        driver.find_element(By.XPATH, '//input[@autocomplete="username"]').send_keys(account)
        driver.find_element(By.XPATH, '//input[@autocomplete="current-password"]').send_keys(password)
        driver.find_element(By.CSS_SELECTOR, '.hhGKQA').click()

    driver.find_element(By.XPATH, '//input[@placeholder="搜索作品"]')
    gl.set_value('btn_text', '打开成功')
    wx.CallAfter(pub.sendMessage, "update")

    phpsessid = driver.get_cookie('PHPSESSID')
    config.set('HttpSession', 'session', phpsessid['value'])
    config.write(open(config_path, 'w', encoding='utf-8'))

    if searchMethod == 1:
        driver.get(f'https://www.pixiv.net/users/{username}/illustrations')
        driver.find_element(By.CSS_SELECTOR, nodes[searchMethod])
        username = driver.find_element(By.CSS_SELECTOR, 'h1.ibhMns').text
    else:
        driver.find_element(By.XPATH, '//input[@placeholder="搜索作品"]').send_keys(username)
        driver.find_element(By.XPATH, '//input[@placeholder="搜索作品"]').send_keys(Keys.ENTER)

        if ageType == 2:
            driver.find_element(By.CSS_SELECTOR, '.bduUXU>div>a:nth-child(2)').click()
            driver.refresh()
            driver.find_element(By.CSS_SELECTOR, nodes[searchMethod])
        elif ageType == 3:
            driver.find_element(By.CSS_SELECTOR, '.bduUXU>div>a:nth-child(3)').click()
            driver.refresh()
            driver.find_element(By.CSS_SELECTOR, nodes[searchMethod])

    async def data_processing(x, index):
        driver.implicitly_wait(0.1)
        num = x.find_elements(By.CSS_SELECTOR, '.kZlOCw>span:nth-child(2)')
        alt = x.find_element(By.CSS_SELECTOR, 'img').get_attribute('alt')
        urls = address_conversion(x.find_element(By.CSS_SELECTOR, 'img').get_attribute('src'),
                                  int(num[0].text if num else 1))
        gl.set_value('total', gl.get_value('total') + len(urls))
        wx.CallAfter(pub.sendMessage, "update")
        for i, src in enumerate(urls):
            await get_img(src, name_processing(f'{index}-{alt}-{i}'), username)

    async def pages():
        global page
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        node_a = driver.find_elements(By.CSS_SELECTOR, 'section ul a.iUsZyY')

        tasks = []
        for i, node in enumerate(node_a):
            tasks.append(data_processing(node, i))
        await asyncio.gather(*tasks)
        if driver.find_element(By.CSS_SELECTOR, 'nav.kYtoqc a:last-child').is_displayed():
            driver.find_element(By.CSS_SELECTOR, 'nav.kYtoqc a:last-child').click()
            driver.refresh()
            driver.find_element(By.CSS_SELECTOR, nodes[searchMethod])
            page += 1
            await pages()
        else:
            gl.set_value('btn_text', '下载完成')
            wx.CallAfter(pub.sendMessage, "update")

    gl.set_value('btn_text', '正在下载')
    wx.CallAfter(pub.sendMessage, "update")
    asyncio.run(pages())
# if __name__ == '__main__':
#     asyncio.run(pages())
