# bs4 사용
from bs4 import BeautifulSoup
#셀레니움 사용 라이브러리
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 크롬 드라이버 경로 설정과 드라이버 설정
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
keywords = "동서대학교"
url ="https://www.naver.com/"
driver.get(url)
driver.implicitly_wait(5)

search_box=driver.find_element(By.ID,"query")
search_box.click()
search_box.send_keys(keywords)
search_box.submit()
# view -> 블로그
driver.find_element(By.CSS_SELECTOR,"#lnb > div.lnb_group > div > ul > li:nth-child(2) > a").click()
driver.find_element(By.CSS_SELECTOR,"#snb > div.api_group_option_filter._search_option_simple_wrap > div > div.option_area.type_sort > a:nth-child(2)").click()

full_html = driver.page_source

soup= BeautifulSoup(full_html,'html.parser')
title_list = soup.find_all('a','api_txt_lines total_tit')
getlist = soup.find('ul', class_='lst_total')

for i in getlist:
    print(i.text.strip())
    print("\n")
input("입력시 종료")