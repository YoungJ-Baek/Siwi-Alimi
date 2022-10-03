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

def generateChecklistCurrent(date=None, type=None, location=None, restriction=None, alternative=None, detail=None):
    checklist = []
    if date is not None: checklist.append(0)
    if type is not None: checklist.append(1)
    if location is not None: checklist.append(2)
    if restriction is not None: checklist.append(3)
    if alternative is not None: checklist.append(4)
    if detail is not None: checklist.append(5)
    
    return checklist

def generateChecklistFuture(date=None, type=None, restriction=None, location=None, detail=None):
    checklist = []
    if date is not None: checklist.append(0)
    if type is not None: checklist.append(1)
    if restriction is not None: checklist.append(2)
    if location is not None: checklist.append(3)
    if detail is not None: checklist.append(4)
    
    return checklist

def parseWebSite(driver=None, url=None):
    driver.get(url)
    driver.implicitly_wait(3)

    html = driver.page_source
    soup = Soup(html, 'html.parser')

    return soup

def getNewInfo(soup=None, checklist=None, date=None, type=None, location=None, restriction=None, alternative=None, detail=None, flag='current'):
    raw_information = soup.find_all('td', 'last')
    sub_length = 6 if flag == 'current' else 5 if flag == 'future' else None
    main_length = int(len(raw_information)/sub_length)

    for index in range(0, main_length):
        for subIndex in range(0, sub_length):
            if subIndex in checklist:
                str_information = str(raw_information[int(index*sub_length+subIndex)])
                formatStart = [m.start() for m in re.finditer('<', str_information)]
                formatEnd = [m.start() for m in re.finditer('>', str_information)]
                str_information = preprocessRaw(str_information=str_information, formatStart=formatStart, formatEnd=formatEnd)
                if flag == 'current':
                    if subIndex == 0: date.append(str_information)
                    elif subIndex == 1: type.append(str_information)
                    elif subIndex == 2: location.append(str_information)
                    elif subIndex == 3: restriction.append(str_information)
                    elif subIndex == 4: alternative.append(str_information)
                    elif subIndex == 5: detail.append(str_information.replace('\n', ' '))
                elif flag == 'future':
                    if subIndex == 0: date.append(str_information)
                    elif subIndex == 1: type.append(str_information)
                    elif subIndex == 2: restriction.append(str_information)
                    elif subIndex == 3: location.append(str_information)
                    elif subIndex == 4: detail.append(str_information.replace('\n', ' '))
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

def compareTwoDetail(detail1=None, detail2=None, event_list_current=None, event_list_future=None):
    compare_list = []
    for index in event_list_current:
        for subIndex in event_list_future:
            if detail2[subIndex] == detail1[index]:
                compare_list.append(subIndex)

    return compare_list

if __name__ == "__main__":
    url_current = 'https://topis.seoul.go.kr/map/openAccMap.do'
    url_future = 'https://topis.seoul.go.kr/map/openControlMap.do'

    type_list = ['집회및행사(집회/시위)', '집회및행사(행사)', '공사', '차량고장', '교통사고'] # add restriction types as many as possible
    keyword = type_list[0]
    date, type, location, restriction, alternative, detail = [], [], None, [], None, [] # create lists for the information
    date_next, type_next, restriction_next, location_next, detail_next = [], [], [], None, []
    checklist_current = generateChecklistCurrent(date=date, type=type, restriction=restriction, detail=detail)
    checklist_future = generateChecklistFuture(date=date_next, type=type_next, restriction=restriction_next, detail=detail_next)

    options = initializeChromeOption()
    driver = mountChromeBrowser(options=options)

    while(1):
        soup_current = parseWebSite(driver=driver, url=url_current)
        date, type, location, restriction, alternative, detail =  getNewInfo(soup=soup_current, checklist=checklist_current, date=date, type=type, restriction=restriction, detail=detail, flag='current')
        event_list_current = extractTypeEvent(keyword=keyword, type=type)
        
        soup_future = parseWebSite(driver=driver, url=url_future)
        date_next, type_next, location_next, restriction_next, alternative_next, detail_next =  getNewInfo(soup=soup_future, checklist=checklist_future, date=date_next, type=type_next, restriction=restriction_next, detail=detail_next, flag='future')
        print(date_next)
        print(type_next)
        print(location_next)
        print(restriction_next)
        print(alternative_next)
        print(detail_next)
        event_list_future = extractTypeEvent(keyword=keyword, type=type_next)
        compare_list = compareTwoDetail(detail1=detail, detail2=detail_next, event_list_current=event_list_current, event_list_future=event_list_future)
        print(event_list_future)
        count = 1
        for index in event_list_current:
            print(f'{index}.\t 기간:\t{date[index]}')
            print(f'\t 유형/통제:\t{type[index]}/{restriction[index]}')
            print(f'\t 세부 사항:\t{detail[index]}')
            count += 1

        count = 1
        for index in event_list_future:
            if index not in compare_list:
                print(f'{count}.\t 기간:\t{date_next[index]}')
                print(f'\t 유형/통제:\t{type_next[index]}/{restriction_next[index]}')
                print(f'\t 세부 사항:\t{detail_next[index]}')
                count += 1
    
        date, type, location, restriction, alternative, detail = prepareNextParsing(secs=120, date=date, type=type, restriction=restriction, detail=detail)
        date_next, type_next, location_next, restriction_next, alternative_next, detail_next = prepareNextParsing(secs=120, date=date_next, type=type_next, restriction=restriction_next, detail=detail_next)

