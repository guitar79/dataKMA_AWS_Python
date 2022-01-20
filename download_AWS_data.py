# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

#크롬 브라우져 열기
driver = webdriver.Chrome(executable_path='./chromedriver_linux64')
#driver=webdriver.Chrome()

#페이지 URL
driver.get('https://data.kma.go.kr/data/grnd/selectAsosList.do?pgmNo=35')

#log=driver.find_element_by_id('loginBtn')
#로그인
log=driver.find_element_by_css_selector('#loginBtn')
sleep(1)
log.click()

logid=driver.find_element_by_name('loginId')
logid.send_keys('guitar79@naver.com')
logpw=driver.find_element_by_name('passwordNo')
logpw.send_keys('pkh19255102!')
logpw.send_keys(Keys.RETURN)
sleep(1)

#100개씩 출력하도록 선택
box=driver.find_element_by_css_selector('#content > div.btn-area > span:nth-child(2)')
box.click()
ActionChains(driver).send_keys(Keys.END).send_keys(Keys.RETURN).perform()
sleep(1)

#검색 클릭 btn-area text-center
search=driver.find_element_by_css_selector('#schForm > div.btn-area.text-center > a:nth-child(1)')
search.click()
sleep(1)

#에러가 생긴 경우 다음 10페이지 부터 받기 위해 10페이지씩 이동
for j in range(0,1):
    if j > 0 :
        next_ten_page=driver.find_element_by_css_selector('#content > div.boardWrap > div > div.pagination.pagination-small > ul > li:nth-child(13) > a')
        next_ten_page.click()
        sleep(1)
    start = j
    print ('%s*10 - page passed ++++++++++\n' % (start))

for ii in range(start,131):
    for i in range(1,11):
        #다음 페이지로 이동
        next_page=driver.find_element_by_css_selector('#content > div.boardWrap > div > div.pagination.pagination-small > ul > li:nth-child(%s) > a' %(i+2))
        next_page.click()
        sleep(1)
        
        check=driver.find_element_by_id('checkAll')
        check.click()
        sleep(1)
        
        #다운로드 클릭
        down=driver.find_element_by_css_selector('#schForm > div.btn-area.text-center > a:nth-child(2)')
        down.click()
        sleep(1)
            
        btn=driver.find_element_by_css_selector('#reqstPurposeCd7')
        btn.click()
        sleep(1)
        
        conf=driver.find_element_by_css_selector('#btnArea > input.btn.btn-primary')
        conf.click()
        sleep(10)
        print ('%s - %s page done ++++++++++\n' % (ii, i))
        
    next_ten_page=driver.find_element_by_css_selector('#content > div.boardWrap > div > div.pagination.pagination-small > ul > li:nth-child(13) > a')
    next_ten_page.click()
    sleep(1)
        
    
    '''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

driver = webdriver.Chrome(executable_path='./chromedriver_linux64')



admin_email = "guitar79@gs.hs.kr"  # 관리자계정입력
admin_passwd = "PASS" # 관리자계정 비번입력
admin_passwd = "Pkh19255102@" # 관리자계정 비번입력

def login_mathwork_admin(admin_email, admin_passwd): 
    driver.get('https://kr.mathworks.com/login?uri=%2Fmwaccount%2F')
    driver.implicitly_wait(3)
    print("debug-driver.implicitly_wait(3)")
    
    frame = driver.find_element_by_id('me')
    driver.switch_to.frame(frame)
    print("debug-driver.switch_to.frame(frame)")
    sleep(1)
    
    driver.find_element_by_id('userId').send_keys(admin_email)
    driver.find_element_by_id('userId').send_keys(Keys.RETURN)
    print("debug-driver.find_element_by_id('userId').send_keys(Keys.RETURN)")
    sleep(1)
    
    driver.find_element_by_id('password').send_keys(admin_passwd)
    driver.find_element_by_id('password').send_keys(Keys.RETURN)
    print("debug-driver.find_element_by_id('password').send_keys(Keys.RETURN)")
    sleep(1)
    return 0

def add_user(first_n, last_n, user_account): 
    license_no = "40449242"
    driver.get('https://kr.mathworks.com/licensecenter/users')
    sleep(1)
    driver.find_element_by_partial_link_text("사용자 추가").click()
    sleep(1)
    
    license_id = driver.find_element_by_id('lid')
    license_id.send_keys(license_no)
    license_id.send_keys(Keys.RETURN)
    sleep(1)
    
    driver.find_element_by_id('forms_add_user_first_name').send_keys(first_n)
    driver.find_element_by_id('forms_add_user_last_name').send_keys(last_n)
    
    driver.find_element_by_id('forms_add_user_latin_family_name').send_keys("GSHS")
    driver.find_element_by_id('forms_add_user_latin_given_name').send_keys("Teacher")
    
    user_email = driver.find_element_by_id('forms_add_user_email_address')
    user_email.send_keys(user_account)
    user_email.send_keys(Keys.RETURN)
    #sleep(1)
    driver.implicitly_wait(1)
    
    driver.find_element_by_partial_link_text("사용자 추가").click()
    sleep(1)
    return 0

f = open("add_user_list_teacher.txt", 'r')
lines = f.readlines()

login_mathwork_admin(admin_email, admin_passwd)
for user_id in lines:
    try : 
        user_id = user_id.replace(" ","")
        user_id = user_id.replace("\n","")
        user_id = user_id.replace("\t","")
        user_id = user_id.split(",")
        print(user_id)
        add_user(user_id[0], user_id[1], user_id[2])
    except :
        continue
    '''
    