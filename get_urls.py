import requests
import lxml.etree as ET
from DrissionPage import ChromiumPage
import time
from DrissionPage.common import By

driver = ChromiumPage()

driver.get('https://www.gravityperformance.co.uk/lowering-springs/')
page = 1
while True:
    time.sleep(5)
    dom = ET.HTML(driver.html)
    containers = dom.xpath('//h2/a/@href')
    with open('urls.txt', 'a') as f:
        for container in containers:
            f.write(f'{container}\n')
    print(f'Page {page} done')
    page = page + 1
    if len(containers) < 24:
        break
    try:
        next_page = (By.XPATH,'//a[@data-value="next"]')
        button = driver.ele(next_page)
        button.click()
    except:
        break

