from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from time import sleep

#크롬 브라우져 열기
#driver = webdriver.Chrome()
driver = webdriver.Chrome(executable_path='./chromedriver_linux64')

#페이지 URL
driver.get('https://data.kma.go.kr/data/grnd/selectAsosList.do?pgmNo=34')

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

#전체선택 클릭
driver.get('https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36&tabNo=1')

select_time = Select(driver.find_element_by_css_selector('#dataFormCd'))

# select by visible text
select_time.select_by_visible_text('분 자료')
#select_time.click()
sleep(1)

search_area = driver.find_element_by_css_selector('#ztree_1_check')
search_area.click()
sleep(1)


search_bt = driver.find_element_by_css_selector('#dsForm > div.wrap_btn > button')
search_bt.click()
sleep(1)

#에러가 생긴 경우 다음 10페이지 부터 받기 위해 10페이지 이동
for j in range(0, 1):
    if j > 0 :
        next_ten_page = driver.find_element_by_css_selector('#wrap_content > div.wrap_itm.area_data > div.cont_itm > div.ft_lst > div.wrap_paging > ul > li.next > a')
        next_ten_page.click()
        sleep(1)     
    start = j
    print ('starting download %s*10 - pages ++++++++++\n' % (start))

for ii in range(start, 5000):
    for i in range(1, 11):
        if i > 1 :
            # 페이지로 이동
            next_page=driver.find_element_by_css_selector('#wrap_content > div.wrap_itm.area_data > div.cont_itm > div.ft_lst > div.wrap_paging > ul > li:nth-child({}) > a'.format(str(i+2)))
            next_page.click()
            sleep(1)
        
        #모두 선택
        check_all = driver.find_element_by_css_selector('#checkAll')
        check_all.click()
        sleep(1)
        
        #다운로드
        dn_checked = driver.find_element_by_css_selector('#wrap_content > div.wrap_itm.area_data > div.cont_itm > div.ft_lst > div.right > a')
        dn_checked.click()
        sleep(1)

        dn_clk1 = driver.find_element_by_css_selector('#requestForm > ul > li:nth-child(15) > label')
        
        dn_clk1.click()
        sleep(1)

        dn_clk2 = driver.find_element_by_css_selector('#wrap-datapop > div > div.cont_layer.box > div > a.btn_request')
        dn_clk2.click()
        sleep(10)
        
        print ('%s - %s page done ++++++++++\n' % (ii, i))
        
    next_ten_page = driver.find_element_by_css_selector('#wrap_content > div.wrap_itm.area_data > div.cont_itm > div.ft_lst > div.wrap_paging > ul > li.next > a')
    next_ten_page.click()
    sleep(1)    