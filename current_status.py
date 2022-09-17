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
driver.get('https://topis.seoul.go.kr/map/openAccMap.do')
driver.implicitly_wait(3)

html = driver.page_source
soup = Soup(html, 'html.parser')

raw_information = soup.find_all('td', 'last')
length = int(len(raw_information)/6)
typeList = ['집회및행사', '공사', '차량고장', '교통사고'] # add restriction types as many as possible

# create lists for the information
date = []
type = []
restriction = []
detail = []

# preprocessing and update the raw information
for index in range(0, length):
    for subIndex in range(0, 6):
        if subIndex in [0, 1, 3, 5]:
            str_information = str(raw_information[int(index*6+subIndex)])
            formatStart = [m.start() for m in re.finditer('<', str_information)]
            formatEnd = [m.start() for m in re.finditer('>', str_information)]
            for formatIndex in range(0, len(formatStart)):
                str_information = str_information.replace(str_information[formatStart[formatIndex]:formatEnd[formatIndex]+1], '', 1)
                for formatUpdate in range(formatIndex+1, len(formatStart)):
                    formatStart[formatUpdate] -= formatEnd[formatIndex] - formatStart[formatIndex] + 1
                    formatEnd[formatUpdate] -= formatEnd[formatIndex] - formatStart[formatIndex] + 1
            if subIndex == 0: date.append(str_information)
            elif subIndex == 1: type.append(str_information)
            elif subIndex == 3: restriction.append(str_information)
            elif subIndex == 5: detail.append(str_information.replace('\n',' '))
        else:
            pass

for index in range(0, len(date)):
    print(f'{index}.\t 기간:\t{date[index]}')
    print(f'\t 유형/통제:\t{type[index]}/{restriction[index]}')
    print(f'\t 세부 사항:\t{detail[index]}')