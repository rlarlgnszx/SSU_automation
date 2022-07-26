# --utf8--#
from http import cookies
from optparse import Option
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import bs4
import json

options = webdriver.ChromeOptions()
# options.add_argument('window-size=1920,1080')
# id = input("id : ")
id = '20180354'
# pw = input("pw : ")
pw = '61296129kh@'
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome('chromedriver.exe', options=options)
driver.get('https://class.ssu.ac.kr')

#! page loding
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/main/div/div[1]/div/div[2]/div[2]/a')))

login_button = driver.find_element(
    by="xpath", value='/html/body/main/div/div[1]/div/div[2]/div[2]/a')
login_button.click()

##put id and pw
WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH,'//*[@id="userid"]')))

put_id = driver.find_element(by="xpath", value='//*[@id="userid"]')
put_pw = driver.find_element(by="xpath", value='//*[@id="pwd"]')

put_id.send_keys(id)
put_pw.send_keys(pw)

id_save = driver.find_element(by='xpath', value='//*[@id="chkSave"]')
id_save.click()
login_click = driver.find_element(
    by='xpath', value='//*[@id="sLogin"]/div/div[1]/form/div/div[2]/a')
login_click.click()

#! wait mypage 
WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH,'/html/body/main/div/div[2]/div[1]/div/div[1]/a')))

mypage = driver.find_element_by_xpath(
    '/html/body/main/div/div[2]/div[1]/div/div[1]/a')
mypage.click()
# * goto mypage 
#! frame change for wait frame
WebDriverWait(driver,4).until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]')))

driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
main_window = driver.current_window_handle

WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/div/div/div[2]/p/span[2]')))
#! how many class you take?
class_num = driver.find_element(by='xpath',value='/html/body/div/div/div/div/div[2]/p/span[2]')
class_num = int(class_num.text.split("/")[1].strip())
class_name= driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div/div[1]/div[1]/div/p').text
all_class = dict()

for x in range(class_num):
    url = '//*[@id="root"]/div/div/div/div[2]/div/div[{}]'.format(x+1)
    class_contain = driver.find_element_by_xpath(url)
    class_name = driver.find_element_by_xpath(url +'/div[1]/div[1]/div/p').text
    class_url = driver.find_element_by_xpath(url +'/div[1]/a').get_attribute('href')
    class_rest_num = driver.find_elements_by_xpath(url +"/div[2]/div[1]/div[2]/div")
    all_class[class_name]={'url':class_url, 'video':[],'assignment':[],'video_conference':[]}
    
    for i in range(len(class_rest_num)):
        sub_url = '/div[2]/div[1]/div[2]/div[{}]'.format(i+1)
        class_rest_name=  driver.find_element_by_xpath(url + sub_url+ "/div[1]").text
        class_rest_day = driver.find_element_by_xpath(url + sub_url+ "/div[2]/div/span").text
        class_rest_direct_url = driver.find_element_by_xpath(url + sub_url+ "/div[1]/a").get_attribute("href")
        classify = driver.find_element_by_xpath(url +sub_url + "/div[1]/i").get_attribute("class")
        classify = classify.split()[1]
        all_class[class_name][classify].append({class_rest_name:{'day':class_rest_day,'url':class_rest_direct_url}})

    # res = session.get('https://canvas.ssu.ac.kr/cours/es/14789/external_tools/2')
    # print(res.text)
    rest_class_video = []
    rest_class_video_conference = []
    rest_class_assignment = []
    for classname in all_class:
        rest_class_video.append(all_class[classname]['video'])
        rest_class_video_conference.append(all_class[classname]['video_conference'])
        rest_class_assignment.append(all_class[classname]['assignment'])
    print(rest_class_video)
    print(rest_class_assignment)
    print(rest_class_video_conference)
    
# 아래부분 동영상 트는것 코드만 더짜면 된다.
print(all_class)
video_len_url = '//*[@id="xnu-component-container-1751933"]/div[2]/div[1]/div[1]/span[2]/span[3]'
#text
click_button_url = '//*[@id="front-screen"]/div/div[2]/div[1]/div'

check_class_url ='//*[@id="xnu-component-container-1751933"]/div[2]/div[3]/div/span[4]'

#text
# xnsti-left-icon video = 강의
# xnsti-left-icon assignment = 과제 
# xnsti-left-icon video_conference = 화상강의
# xn-student-todo-item-container  =  남은거


# /html/body/div/div/div/div/div[2]/div/div[4]/div[1]/a


#id 속성으로 접근
# driver.find_element_by_id('btn_login_action').click()    #링크가 달려 있는 텍스트로 접근

# time.sleep(3)
# driver.find_element_by_class_name('pop_alert').click()
# time.sleep(0.5)
# driver.find_element_by_class_name('right').click()
# driver.find_element_by_class_name('left').click()
# time.sleep(0.5)
# driver.find_element_by_class_name('right').click()

# driver.find_element_by_class_name('right').click()

#class 속성으로 접근

# btn_close
# driver.find_element_by_css_selector('#account > div > a')   #css 셀렉터로 접근
# driver.find_element_by_name('join') #name 속성으로 접근
# driver.find_element_by_partial_link_text('가입')  #링크가 달려 있는 엘레먼트에 텍스트 일부만 적어서 해당 엘레먼트에 접근
# driver.find_element_by_tag_name('input')    #태그 이름으로 접근

# driver.find_element_by_tag_name('input').find_element_by_tag_name('a')  #input 태그 하위태그인 a 태그에 접근
# driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div/div[3]/form/fieldset/button/span[2]').find_element_by_name('join') #xpath 로 접근한 엘레먼트의 안에 join 이라는 속성을 가진 tag 엘레먼트에 접근

# driver.find_element_by_id('ke_kbd_btn').click()
# #이동할 프레임 엘리먼트 지정
# element = driver.find_element_by_tag_name('iframe')

#프레임 이동
# driver.switch_to.frame(element)

# #프레임에서 빠져나오기
# driver.switch_to.default_content()

