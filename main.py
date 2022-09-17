import re
from tabnanny import check
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as Soup

def initializeChromeOption():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    return options

def mountChromeBrowser(options=None):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    return driver

def generateChecklist(date=None, type=None, location=None, restriction=None, alternative=None, detail=None):
    checklist = []
    if date is not None: checklist.append(0)
    if type is not None: checklist.append(1)
    if location is not None: checklist.append(2)
    if restriction is not None: checklist.append(3)
    if alternative is not None: checklist.append(4)
    if detail is not None: checklist.append(5)
    
    return checklist

def parseWebSite(driver=None, url=None):
    driver.get(url)
    driver.implicitly_wait(3)

    html = driver.page_source
    soup = Soup(html, 'html.parser')

    return soup

def getNewInfo(soup=None, checklist=None, date=None, type=None, location=None, restriction=None, alternative=None, detail=None):
    raw_information = soup.find_all('td', 'last')
    length = int(len(raw_information)/6)

    for index in range(0, length):
        for subIndex in range(0, 6):
            if subIndex in checklist:
                str_information = str(raw_information[int(index*6+subIndex)])
                formatStart = [m.start() for m in re.finditer('<', str_information)]
                formatEnd = [m.start() for m in re.finditer('>', str_information)]
                str_information = preprocessRaw(str_information=str_information, formatStart=formatStart, formatEnd=formatEnd)
                if subIndex == 0: date.append(str_information)
                elif subIndex == 1: type.append(str_information)
                elif subIndex == 2: location.append(str_information)
                elif subIndex == 3: restriction.append(str_information)
                elif subIndex == 4: alternative.append(str_information)
                elif subIndex == 5: detail.append(str_information.replace('\n', ' '))
            else:
                pass

    return date, type, location, restriction, alternative, detail

def preprocessRaw(str_information=None, formatStart=None, formatEnd=None):
    for formatIndex in range(0, len(formatStart)):
        str_information = str_information.replace(str_information[formatStart[formatIndex]:formatEnd[formatIndex]+1], '', 1)
        for formatUpdate in range(formatIndex+1, len(formatStart)):
            formatStart[formatUpdate] -= formatEnd[formatIndex] - formatStart[formatIndex] + 1
            formatEnd[formatUpdate] -= formatEnd[formatIndex] - formatStart[formatIndex] + 1
    
    return str_information

def prepareNextParsing(secs=60, date=None, type=None, location=None, restriction=None, alternative=None, detail=None):
    time.sleep(secs)
    if date is not None: date.clear()
    if type is not None: type.clear()
    if location is not None: location.clear()
    if restriction is not None: restriction.clear()
    if alternative is not None: alternative.clear()
    if detail is not None: detail.clear()

    return date, type, location, restriction, alternative, detail

def extractTypeEvent(keyword=None, type=None):
    event_list = []
    for index in range(0, len(type)):
        if type[index].find(keyword) != -1:
            event_list.append(index)
    
    return event_list

def compareTwoDetail(detail1=None, detail2=None, event_list=None):
    compare_list = []
    for index in event_list:
        for subIndex in range(0, len(detail2)):
            if detail2[subIndex] == detail1[index]:
                compare_list.append(subIndex)

    return compare_list
    
if __name__ == "__main__":
    url_current = 'https://topis.seoul.go.kr/map/openAccMap.do'
    url_future = 'https://topis.seoul.go.kr/map/openControlMap.do'

    type_list = ['집회및행사', '공사', '차량고장', '교통사고'] # add restriction types as many as possible
    date, type, location, restriction, alternative, detail = [], [], None, [], None, [] # create lists for the information
    date_next, type_next, location_next, restriction_next, alternative_next, detail_next = [], [], None, [], None, []
    checklist = generateChecklist(date=date, type=type, restriction=restriction, detail=detail)

    options = initializeChromeOption()
    driver = mountChromeBrowser(options=options)

    while(1):
        soup_current = parseWebSite(driver=driver, url=url_current)
        date, type, location, restriction, alternative, detail =  getNewInfo(soup=soup_current, checklist=checklist, date=date, type=type, restriction=restriction, detail=detail)
        event_list = extractTypeEvent(type_list[0], type)
        
        soup_future = parseWebSite(driver=driver, url=url_future)
        date_next, type_next, location_next, restriction_next, alternative_next, detail_next =  getNewInfo(soup=soup_future, checklist=checklist, date=date_next, type=type_next, restriction=restriction_next, detail=detail_next)
        compare_list = compareTwoDetail(detail1=detail, detail2=detail_next, event_list=event_list)

        for index in event_list:
            print(f'{index}.\t 기간:\t{date[index]}')
            print(f'\t 유형/통제:\t{type[index]}/{restriction[index]}')
            print(f'\t 세부 사항:\t{detail[index]}')
        
        # for index in range(0, len(date_next)):
        #     if index not in compare_list:
        #         print(f'{index}.\t 기간:\t{date_next[index]}')
        #         print(f'\t 유형/통제:\t{type_next[index]}/{restriction_next[index]}')
        #         print(f'\t 세부 사항:\t{detail_next[index]}')
    
        date, type, location, restriction, alternative, detail = prepareNextParsing(secs=120, date=date, type=type, restriction=restriction, detail=detail)
        date_next, type_next, location_next, restriction_next, alternative_next, detail_next = prepareNextParsing(secs=120, date=date_next, type=type_next, restriction=restriction_next, detail=detail_next)
