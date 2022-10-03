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

def parseWebSite(driver=None, url=None):
    driver.get(url)
    driver.implicitly_wait(3)

    html = driver.page_source
    soup = Soup(html, 'html.parser')

    return soup

def getEventInfo(soup=None, checklist=None, date=None, type=None, location=None, restriction=None, alternative=None, detail=None):
    raw_information = soup.find_all('td', 'last')
    sub_length = 6
    main_length = int(len(raw_information)/sub_length)

    for index in range(0, main_length):
        for subIndex in range(0, sub_length):
            if subIndex in checklist:
                str_information = str(raw_information[int(index*sub_length+subIndex)])
                formatStart = [m.start() for m in re.finditer('<', str_information)]
                formatEnd = [m.start() for m in re.finditer('>', str_information)]
                str_information = preprocessRaw(str_information=str_information, formatStart=formatStart, formatEnd=formatEnd)
                if subIndex == 0: date.append(str_information)
                elif subIndex == 1: type.append(str_information)
                elif subIndex == 2: location.append(str_information)
                elif subIndex == 3: restriction.append(str_information)
                elif subIndex == 4: alternative.append(str_information)
                elif subIndex == 5: detail.append(str_information.replace('\n', ' '))
                else: pass
        
    return date, type, location, restriction, alternative, detail

def getProtestInfo(soup=None, checklist=None, date=None, type=None, location=None, restriction=None, alternative=None, detail=None, flag=None):
    target = 'PROG' if flag == 'current' else 'PLAN' if flag == 'future' else None
    raw_information = soup.find_all('ul', {'id': target})[0].find_all('td', 'last')
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
                    elif subIndex == 2: restriction.append(str_information)
                    elif subIndex == 3: alternative.append(str_information)
                    elif subIndex == 4: location.append(str_information)
                    elif subIndex == 5: detail.append(str_information.replace('\n', ' '))
                elif flag == 'future':
                    if subIndex == 0: date.append(str_information)
                    elif subIndex == 1: type.append(str_information)
                    elif subIndex == 2: restriction.append(str_information)
                    elif subIndex == 3: location.append(str_information)
                    elif subIndex == 4: detail.append(str_information.replace('\n', ' '))
            else:
                pass
    
    return date, type, restriction, alternative, location, detail

def preprocessRaw(str_information=None, formatStart=None, formatEnd=None):
    for formatIndex in range(0, len(formatStart)):
        str_information = str_information.replace(str_information[formatStart[formatIndex]:formatEnd[formatIndex]+1], '', 1)
        for formatUpdate in range(formatIndex+1, len(formatStart)):
            formatStart[formatUpdate] -= formatEnd[formatIndex] - formatStart[formatIndex] + 1
            formatEnd[formatUpdate] -= formatEnd[formatIndex] - formatStart[formatIndex] + 1
    
    return str_information

def generateChecklistEvent(date=None, type=None, location=None, restriction=None, alternative=None, detail=None):
    checklist = []
    if date is not None: checklist.append(0)
    if type is not None: checklist.append(1)
    if location is not None: checklist.append(2)
    if restriction is not None: checklist.append(3)
    if alternative is not None: checklist.append(4)
    if detail is not None: checklist.append(5)
    
    return checklist

def generateChecklistProtest(date=None, type=None, restriction=None, alternative=None, location=None, detail=None, flag=None):
    checklist = []
    if date is not None: checklist.append(0)
    if type is not None: checklist.append(1)
    if restriction is not None: checklist.append(2)
    if flag == 'current':
        if alternative is not None: checklist.append(3)
        if location is not None: checklist.append(4)
        if detail is not None: checklist.append(5)
    elif flag == 'future':
        if location is not None: checklist.append(3)
        if detail is not None: checklist.append(4)
    
    return checklist

def getEvent():
    options = initializeChromeOption()
    driver = mountChromeBrowser(options=options)

    url_event = 'https://topis.seoul.go.kr/map/openAccMap.do'
    date, type, location, restriction, alternative, detail = [], [], None, [], None, [] # create lists for the event information
    checklist_event = generateChecklistEvent(date=date, type=type, restriction=restriction, detail=detail)

    soup_event = parseWebSite(driver=driver, url=url_event)
    date, type, location, restriction, alternative, detail =  getEventInfo(soup=soup_event, checklist=checklist_event, date=date, type=type, restriction=restriction, detail=detail)
    
    result, count = "", 1
    for index in range(0, len(date)):
        result += f'{count}. 기간: {date[index]}\n'
        result += f'유형/통제: {type[index]}/{restriction[index]}\n'
        result += f'세부 사항: {detail[index]}\n'
        count += 1
    
    return result

def getProtest(flag=None):
    options = initializeChromeOption()
    driver = mountChromeBrowser(options=options)

    url_protest = 'https://topis.seoul.go.kr/map/openControlMap.do'
    date, type, location, restriction, alternative, detail = [], [], None, [], None, [] # create lists for the current protest information
    checklist_protest = generateChecklistProtest(date=date, type=type, restriction=restriction, detail=detail, flag=flag)

    soup_protest = parseWebSite(driver=driver, url=url_protest)
    date, type, restriction, alternative, location, detail = getProtestInfo(soup=soup_protest, checklist=checklist_protest, date=date, type=type, restriction=restriction, detail=detail, flag=flag)

    result, count = "", 1
    for index in range(0, len(date)):
        result += f'{count}. 기간: {date[index]}\n'
        result += f'유형/통제: {type[index]}/{restriction[index]}\n'
        result += f'세부 사항: {detail[index]}\n'
        count += 1

    return result

def getCurrentProtest():
    try:
        return getProtest('current')
    except IndexError:
        return '현재 집회 및 시위가 없습니다.'

def getFutureProtest():
    return getProtest('future')

def legacy():
    url_event = 'https://topis.seoul.go.kr/map/openAccMap.do'
    url_protest = 'https://topis.seoul.go.kr/map/openControlMap.do'

    type_list = ['집회및행사(집회/시위)', '집회및행사(행사)', '공사', '차량고장', '교통사고'] # add restriction types as many as possible
    keyword = type_list[0]
    dateE, typeE, locationE, restrictionE, alternativeE, detailE = [], [], None, [], None, [] # create lists for the event information
    dateP, typeP, restrictionP, locationP, detailP = [], [], [], None, []
    checklist_current = generateChecklistEvent(date=dateE, type=typeE, restriction=restrictionE, detail=detailE)
    checklist_future = generateChecklistProtest(date=dateP, type=typeP, restriction=restrictionP, detail=detailP)

    options = initializeChromeOption()
    driver = mountChromeBrowser(options=options)

    while(1):
        soup_event = parseWebSite(driver=driver, url=url_event)
        soup_protest = parseWebSite(driver=driver, url=url_protest)
        c = soup_current.find_all('ul', {'id':'PROG'})
        raw_information = c[0].find_all('td', 'last')
        print(raw_information[1])
        exit()
        date, type, location, restriction, alternative, detail =  getNewInfo(soup=soup_current, checklist=None, date=date, type=type, restriction=restriction, detail=detail, flag='current')
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

def main():
    print(getEvent())
    print(getCurrentProtest())
    print(getFutureProtest())

if __name__ == "__main__":
    main()