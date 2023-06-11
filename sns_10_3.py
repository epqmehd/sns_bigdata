# 사용자에게 검색어와 저장할 파일들의 경로를 입력받은 후 
# 해당 키워드로 검색하여 나오는 결과에서 블로그만 선택한 후 
# 처음 1페이지에 있는 결과 10건의 게시물에서 아래 예시와 같이 txt형식의 파일로 저장을 하고, 표로 만들어서 xls, csv 형식으로 저장하세요.

# bs4 사용
from bs4 import BeautifulSoup
#셀레니움 사용 라이브러리
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# 사용 라이브러리
import os
import pandas as pd 
import xlwt # 엑셀
# 크롬 드라이버 경로 설정
driver = webdriver.Chrome(ChromeDriverManager().install())
# 사용자에게 검색어와 저장할 파일들의 경로 입력 받기
keyword = input("크롤링할 키워드를 입력하세요 : ")
path_folder = input("파일들을 저장할 폴더 경로 입력 : ")

txt_filename = input('저장할 txt 파일 이름을 지정하세요 : ') + ".txt"
csv_filename = input('저장할 csv 파일 이름을 지정하세요 : ') + '.csv'
xlsx_filename = input('저장할 xls 파일 이름을 지정하세요 : ') + '.xlsx'

txt_path = os.path.join(path_folder, txt_filename)
csv_path = os.path.join(path_folder, csv_filename)
xlsx_path = os.path.join(path_folder, xlsx_filename)
# 검색시작
url ="https://www.naver.com/"
driver.get(url)
driver.implicitly_wait(5)

search_box=driver.find_element(By.ID,"query")
search_box.click()
search_box.send_keys(keyword)
search_box.submit()
# view -> 블로그 진입
driver.find_element(By.CSS_SELECTOR,"#lnb > div.lnb_group > div > ul > li:nth-child(2) > a").click()
driver.find_element(By.CSS_SELECTOR,"#snb > div.api_group_option_filter._search_option_simple_wrap > div > div.option_area.type_sort > a:nth-child(2)").click()

# 블로그 섹션 텍스트 추출
full_html = driver.page_source
soup = BeautifulSoup(full_html,'html.parser')
content_list = soup.find('ul', class_="lst_total")

# 10건 txt로 저장후 xls,csv형식 저장
# 1. 글번호 2.제목 3.내용 4.작성일자 5. 블로그 닉네임
num = 1
num2 = [ ]
title2 = [ ]
cont2 = [ ]
date2 = [ ]
nick2 = [ ]

count = 0
for i in content_list.find_all('li', "bx"):
    num2.append(num)
    print('번호:',num)
    num += 1
        
    title = i.find('a', 'api_txt_lines total_tit').get_text()
    title2.append(title)
    print('제목:', title.strip())

    cont = i.find('div', 'api_txt_lines dsc_txt').get_text()
    cont2.append(cont)
    print('내용', cont.strip())
        
    date = i.find('span', 'sub_time sub_txt').get_text()
    date2.append(date)
    print('작성날짜:', date.strip())

    nick = i.find('a', 'sub_txt sub_name').get_text()
    nick2.append(nick)
    print('닉네임:', nick.strip())
    print("\n")
    
    count += 1
    if count >= 10:
        break
        
datapd = pd.DataFrame()

datapd['번호'] = num2
datapd['제목'] = title2
datapd['내용'] = cont2
datapd['작성날짜'] = date2
datapd['닉네임'] = nick2

# csv 형태로 저장하기
datapd.to_csv(csv_path, encoding="utf-8-sig")
print(" csv 파일 저장 경로: %s" %csv_path)

# 엑셀 형태로 저장하기
datapd.to_excel(xlsx_path)
print(" xls 파일 저장 경로: %s" %xlsx_path)

# 출력 결과를 txt 파일로 저장하기
f = open(txt_path, 'a', encoding='UTF-8')
f.write(str(title2))
f.write(str(cont2))
f.write(str(date2))
f.write(str(nick2))
f.close( )
print(" txt 파일 저장 경로: %s" %txt_path)  


input("입력시 종료")