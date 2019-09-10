import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException

### 크롬 열기 ###
driver = webdriver.Chrome(r"G:\공유 드라이브\democracy_seoul\02code\chrome\chromedriver.exe")
driver.get('https://eungdapso.seoul.go.kr/Shr/Shr01/Shr01_lis.jsp')


### 변수별 css_selector 확인 ###
title_click = driver.find_element_by_css_selector('#content_cont > div.info_wrap > div > form > div.pclist_table.mt20 > div:nth-child(2) > ul > li.pclist_list_tit42 > a')
title_click.click()
#div:nth-child(2) ~  div:nth-child(11)
#content_cont > div.info_wrap > div > form > div.pclist_table.mt20 > div:nth-child(3) > ul > li.pclist_list_tit42 > a
#content_cont > div.info_wrap > div > form > div.pclist_table.mt20 > div:nth-child(11) > ul > li.pclist_list_tit42 > a

title = driver.find_element_by_css_selector('#content_cont > div.info_wrap > div > table:nth-child(1) > tbody > tr:nth-child(1) > td').text
title

date = driver.find_element_by_css_selector('#content_cont > div.info_wrap > div > table:nth-child(1) > tbody > tr:nth-child(2) > td').text
date

contents = driver.find_element_by_css_selector('#content_cont > div.info_wrap > div > table.table_style.mb10 > tbody > tr > td > div').text
contents

answer = driver.find_element_by_css_selector('#content_cont > div.info_wrap > div > table:nth-child(3) > tbody > tr > td > div > p:nth-child(2)').text
answer

back_to_lists = driver.find_element_by_css_selector('#content_cont > div.info_wrap > div > div > a')
back_to_lists.click()

#pass 2page
#content_cont > div.info_wrap > div > div.pagination > span > a:nth-child(2)
#content_cont > div.info_wrap > div > div.pagination > span > a:nth-child(3)

#next lists
#content_cont > div.info_wrap > div > div.pagination > a
next_lists = driver.find_element_by_css_selector('#content_cont > div.info_wrap > div > div.pagination > a')
next_lists.click()



### Crawling Flow ###
# 1. 10개 포스트 각각 들어가 수집 #
# 2. 다음 페이지로 이동해 포스트 수집 #
# 3. 5개 페이지 모두 수집했다면 다음 리스트로 이동 #
# 4. 1~3 반복 #

#variable initialize
seoul = pd.DataFrame(columns=['title','date','contents','answer'])
n = 10

for list_num in range(1,n): #n번 게시판까지
    print(list_num)
    for title_num in range(2,12): #2~11, 제목
        #민원포스팅별 클릭
        title_selector = f'#content_cont > div.info_wrap > div > form > div.pclist_table.mt20 > div:nth-child({title_num}) > ul > li.pclist_list_tit42 > a'
        title_click = driver.find_element_by_css_selector(title_selector)
        driver.implicitly_wait(20)
        title_click.click()

        #필요 변수 저장
        title = driver.find_element_by_css_selector('#content_cont > div.info_wrap > div > table:nth-child(1) > tbody > tr:nth-child(1) > td').text
        date = driver.find_element_by_css_selector('#content_cont > div.info_wrap > div > table:nth-child(1) > tbody > tr:nth-child(2) > td').text
        contents = driver.find_element_by_css_selector('#content_cont > div.info_wrap > div > table.table_style.mb10 > tbody > tr > td > div').text
        answer = driver.find_element_by_css_selector('#content_cont > div.info_wrap > div > table:nth-child(3) > tbody > tr > td > div > p:nth-child(2)').text
        
        res = pd.DataFrame({'title':[title],'date':[date],'contents':[contents],'answer':[answer]})
        
        #concat
        seoul = pd.concat([seoul,res],ignore_index=True)

        #목록으로 돌아가기
        back_to_lists = driver.find_element_by_css_selector('#content_cont > div.info_wrap > div > div > a')
        driver.implicitly_wait(20)
        back_to_lists.click()    

    if int(driver.find_element_by_css_selector('#content_cont > div.info_wrap > div > div.pagination > span > a.on').text)%5 != 0:
        # click next page
        next_page_selector = f'#content_cont > div.info_wrap > div > div.pagination > span > a:nth-child({list_num%5+1})'
        next_page=driver.find_element_by_css_selector(next_page_selector)
        driver.implicitly_wait(10)
        next_page.click()
    else:
        # click next lists
        print('next lists')
        if list_num <= 5:
            next_lists = driver.find_element_by_css_selector('#content_cont > div.info_wrap > div > div.pagination > a')
        else:
            next_lists = driver.find_element_by_css_selector('#content_cont > div.info_wrap > div > div.pagination > a.next')
        driver.implicitly_wait(10)
        next_lists.click()

seoul.drop_duplicates(inplace=True) #중복삭제
seoul.to_csv(r'G:\공유 드라이브\democracy_seoul\03output\190809_서울응답소_추가.csv',index=None)