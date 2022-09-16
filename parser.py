import requests
from bs4 import BeautifulSoup as Soup

base_url = 'https://topis.seoul.go.kr/map/openAccMap.do'
flag = '공사/집회'
section = 'd2'
terminate = '<!-- Tab : 사고, 공사 등 통제 종료 -->'

response = requests.get(base_url)
page = response.text
print(page.find('돌발'))
soup = Soup(page, 'html.parser')
text = soup.select('ul.unexinfor > li > a')
print(text)
# information = soup.find_all('div', 'list-group w-list-group w1140', id='accInfo13')
information = soup.find_all('div', 'parktit')
# information = soup.find_all('small', 'label label-warning')
print(information)


# If URL response success, initialilze following parameters
# if response.status_code == 200:
#     page = response.text
#     index_base = page.find(flag)
#     index_section = index_base + page[index_base:].find(section)
#     index_terminate = page.find(terminate)
#     print(page[index_section:index_terminate])

# else:
#     print('URL is not working')
#     exit()