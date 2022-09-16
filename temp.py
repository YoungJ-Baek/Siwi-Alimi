import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as Soup

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# driver.get('https://topis.seoul.go.kr/map/openAccMap.do')
driver.get('https://topis.seoul.go.kr/map/openControlMap.do')
driver.implicitly_wait(3)

html = driver.page_source
soup = Soup(html, 'html.parser')
test = str(soup.find_all('td', 'last')[0])
print(test)
print([m.start() for m in re.finditer('<', test)])
print([m.start() for m in re.finditer('>', test)])



# print(soup.find_all('td', 'last')[0:6])


# temp = driver.find_elements(by=By.CLASS_NAME, value='last')