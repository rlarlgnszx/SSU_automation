import re
from playwright.sync_api import Page, ElementHandle , expect ,sync_playwright
import os
import dotenv
import pickle
import threading
import copy
# import lxml
from ssu import todo_class , SSU
from bs4 import BeautifulSoup as bs
dotenv.load_dotenv()
id = os.environ.get("ID")
pw = os.environ.get("PW")
tododict= {'video':1,'assignment':2,'file':3}
save = SSU
##================================================================================================
def searchID_PW(page:Page,id,pw):
    page.goto('https://class.ssu.ac.kr/mypage')
    # expect(page).to_have_title
    get_started = page.locator('.btn_login')
    expect(get_started).to_have_text('로그인')
    get_id= page.locator('#userid')
    get_pw=page.locator('#pwd')
    get_id.fill(id)
    get_pw.fill(pw)
    get_started.click()
    page.wait_for_url('https://class.ssu.ac.kr/')
    return page

def get_class(page:Page,id):
    global save
    page.goto(f'https://canvas.ssu.ac.kr/learningx/dashboard?user_login={id}&locale=ko')
    page.wait_for_load_state('networkidle')
    page.inner_html('div#root')
    temp = page.get_by_text('모두 펼치기')
    temp.click()
    page.screenshot(path='hee.png')
    html = page.query_selector('//*[@id="root"]/div/div/div[2]/div[2]')
    todo_class_list=  html.query_selector_all('.xn-student-todo-item-container')

    if len(todo_class_list)>=1:
        for i in todo_class_list:
            class_status= i.query_selector('.xnsti-left-icon').get_attribute('class')
            class_title= i.query_selector('.xnsti-left-title')
            class_rest = i.query_selector('.xnsti-right-dday-text').text_content()
            class_url = class_title.get_attribute('href')
            class_title = class_title.text_content()
            save(todo_class(class_title,class_url,class_rest,class_status,page))
    # SSU.showing_todo()
    while 1:
        try:
            SSU.streaming()
            SSU.current_stream+=1
        except IndexError:
            print("all done")
            return
    
    new_class_dict=dict()
    class_todo=page.query_selector_all('.xn-student-todo-item-container');
    class_name = page.query_selector_all('.xnscc-header-title')
    class_url = page.query_selector_all('.xnscc-header-redirect-link')
    all_class=dict()
    for index,name in enumerate(class_name):
        name.select_text()
        url = class_url[index].get_attribute('href')
        class_url[index]
        all_class[name.inner_text()]={"url":url}
    new_dict= dict()   
    return page,all_class

def make_dir(page,classes:dict):
    for i in classes:
        os.makedirs(f'./{i}',exist_ok=True)
        os.makedirs(f"./{i}/files",exist_ok=True)
        os.makedirs(f"./{i}/pdf",exist_ok=True)

def per_class_download(page:Page,class_name,class_url):
    print("##")
    #video = .readystream
    #pdf = .pdf
    #file = .file 
    #과제 =.assignment
    page.goto(class_url+'/external_tools/2')
    page.wait_for_load_state('networkidle')
    frame = page.frame_locator('.tool_launch').get_by_text('모든 주차');
    frame.click()
    class_per_dict=dict()
    class_per_dict['name']=class_name;
    class_per_dict['url'] = class_url;
    per_class_all= page.query_selector("#tool_content").content_frame()
    per_class_all=per_class_all.query_selector_all('.xncb-component-wrapper')
    for index,class_ in enumerate(per_class_all):
        class_status = class_.query_selector('.xncb-component-icon')
        class_title= class_.query_selector('.xncb-component-title').text_content();
        sub_class_rest_time = class_.query_selector('.xncb-component-sub-d_day').text_content();
        # print("=============================")        
        
        # print(class_status.get_attribute("class"))
        # print(class_title)
        # # print(sub_class_title)
        # # if sub_class_rest_start_end:
        # #     print(sub_start)
        # #     print(sub_end)
        # print(sub_class_rest_time)
        
    
    # class_to_do['todo']=
    
# def main_server_shut_down(p:Page,classes_url:list):
#     get_started = p.get_by_role("link", name="모든 과목")
#     print(get_started)
#     expect(get_started).to_have_attribute("href", "/courses/")
#     for class_url in classes_url:
#         per_class_get_todo(p,class_url)
        
    
# def per_class_get_todo(p:Page,class_url):
#     p.goto(p.url+class_url+'/external_tools/2')
#     p.wait_for_load_state('networkidle')
#     frame = p.frame_locator('.tool_launch').get_by_text('모든 주차');
#     frame.click()

def start():
    with sync_playwright() as p:
        for browser_type in [p.chromium]:
            browser = p.chromium.launch(channel='chrome')
            desktop = p.devices["Desktop Chrome"]
            context = browser.new_context(**desktop)
            page = browser.new_page()
            temping = searchID_PW(page,id,pw)
            print("start get class")
            print("server is ok")
            page,classes = get_class(temping,id)
            print("end get class")
            browser.close()
start()