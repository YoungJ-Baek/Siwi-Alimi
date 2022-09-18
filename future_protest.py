import requests
from bs4 import BeautifulSoup

from datetime import date

response = requests.get('https://www.spatic.go.kr/article/view.do?articleId=10556&boardId=4&menuId=21&currentPageNo=1')

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




#contents > div.board_body > table > tbody > tr.content_area > td > table > tbody
#contents > div.board_body > table > tbody > tr.content_area > td > table > tbody > tr:nth-child(1)
#contents > div.board_body > table > tbody > tr.content_area > td > table > tbody > tr:nth-child(2)

#contents > div.board_body > table > tbody > tr.content_area > td > table > tbody > tr:nth-child(2) > td:nth-child(3)
