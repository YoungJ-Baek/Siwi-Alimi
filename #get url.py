#get url
#to get the url of the current today's protest article

from selenium import webdriver
import time
import datetime
from selenium.webdriver.common.by import By

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

url = driver.find_element(By. CSS_SELECTOR, '#contents > div.board_body > table > tbody > tr > td.board_list_title > a').get_attribute('href')

driver.close()

print(url)

#contents > div.board_body > table > tbody > tr:nth-child(1) > td.board_list_title > a

#searchValue#searchValue

#contents > div.board_body > table > tbody > tr > td.board_list_title > a

