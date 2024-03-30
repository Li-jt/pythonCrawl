import asyncio
import os
import configparser

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from utils.index import getRootPath, addressConversion, nameProcessing
from utils.requests.index import get_img

chrome_options = Options()
chrome_options.add_argument("--headless")

# webdriver.ChromeOptions().add_argument('–headless')

nodes = {
    1: '.cDZIoX', 2: 'section ul.hdRpMN', 3: '.cDZIoX'
}

config_path = os.path.join(getRootPath(), "config.ini")

config = configparser.ConfigParser()
config.read(config_path, encoding='utf-8')

searchMethod = int(input('搜索方式(1:画师id;2:搜索;)：'))

username = input('作品或用户id：')
ageType = 2
if searchMethod == 2:
    ageType = int(input('类型（1:全部，2:全年龄，3:R-18）：'))

account = config.get('pixiv', 'account')
password = config.get('pixiv', 'password')

session = config.get('HttpSession', 'session')

# driver = webdriver.Chrome()
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1920, 1080 * 2)

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
    # > div: nth - child(2) > div > span:nth - child(2)
    driver.implicitly_wait(0.1)
    num = x.find_elements(By.CSS_SELECTOR, '.kZlOCw>span:nth-child(2)')
    alt = x.find_element(By.CSS_SELECTOR, 'img').get_attribute('alt')
    urls = addressConversion(x.find_element(By.CSS_SELECTOR, 'img').get_attribute('src'),
                             int(num[0].text if num else 1))
    for i, src in enumerate(urls):
        await get_img(src, nameProcessing(f'{index}-{alt}-{i}'), username)


async def pages():
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
        await pages()


if __name__ == '__main__':
    asyncio.run(pages())
