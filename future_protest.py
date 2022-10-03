import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import datetime
from selenium.webdriver.common.by import By

def get_url_for_protest():
    days = ['월', '화', '수', '목', '금', '토', '일']
    today_month = datetime.datetime.now().month
    today_day = datetime.datetime.now().day
    a = datetime.datetime.today().weekday()
    today_weekday = days[a]

    search_key = str(today_month) + '월 ' + str(today_day) + '일 ' + '(' + (today_weekday) + ') ' + "집회 및 행사"

    driver = webdriver.Chrome(r"C:/Users/qordnrwls/myproject/chromedriver.exe")

    driver.get('https://www.spatic.go.kr/article/list.do?boardId=4&currentPageNo=1&menuId=21&recordCountPerPage=10&searchEtc1=&searchEtc2=&searchEtc3=&searchEtc4=&searchEtc5=&searchSelect=title&searchValue=')

    searchbox = driver.find_element(By. CSS_SELECTOR, '#searchValue')
    searchbox.send_keys(search_key)

    searchbutton = driver.find_element(By. CSS_SELECTOR, '#searchForm > a')
    searchbutton.click()

    result_url = driver.find_element(By. CSS_SELECTOR, '#contents > div.board_body > table > tbody > tr > td.board_list_title > a').get_attribute('href')

    driver.close()

    return(result_url)

#css selector for search box input : #searchValue

#css selector for href of search result : #contents > div.board_body > table > tbody > tr > td.board_list_title > a

response = requests.get(str(get_url_for_protest()))

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    future_protest = ""

    for i in range(2, 15):
        try:
            protest_place = '#contents > div.board_body > table > tbody > tr.content_area > td > table > tbody > tr:nth-child' + '(' + str(i) + ')'
            content = soup.select_one(protest_place)
            content_text = content.get_text()
            future_protest += content_text[:1] + ". " + content_text[1:] + "\n"
        except:
            pass
    print(future_protest)

else : 
    print(response.status_code)



#css selector for "n"th protest content: 
#contents > div.board_body > table > tbody > tr.content_area > td > table > tbody > tr:nth-child(2) > td:nth-child("n")
