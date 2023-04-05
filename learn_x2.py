#-*- coding: utf-8 -*-
import re
from playwright.sync_api import Page, expect, sync_playwright , Browser
import playwright.sync_api as pl
import os
import dotenv
from multiprocessing import Queue, Process ,Manager
from multiprocessing.pool import Pool
import multiprocessing as mp
import requests
import zipfile
import threading
from datetime import datetime
from urllib.parse import urlsplit, parse_qsl
from line import Local
import time
import asyncio
# import ssuUI
#=====================================================
from ssu import SSU
from class_save import main_class,todo_class
# from bs4 import BeautifulSoup as bs
#===================================================
dotenv.load_dotenv()
liner = Local()
id = os.environ.get("ID")
pw = os.environ.get("PW")

TAG_SELECTOR = liner.TAG_SELECTOR
MAIN_URL = liner.MAIN_URL
ID_LOCATOR = liner.ID_LOCATOR
PW_LOCATOR =liner.PW_LOCATOR
GET_CLASS_TODO_CLASS_1_FRAME = liner.GET_CLASS_TODO_CLASS_1_FRAME
FOR_ID_ITME = liner.FOR_ID_ITME
FOR_PW_ITME =liner.FOR_PW_ITME
MY_PAGE= liner.MY_PAGE
PER_URL = liner.PER_URL
PDF_PAGE_SELECTOR =liner.PDF_PAGE_SELECTOR
PDF_1_XPATH =liner.PDF_1_XPATH
PDF_2_XPATH =liner.PDF_2_XPATH
PDF_3_XPATH =liner.PDF_3_XPATH
PDF_URL_LOCATOR =liner.PDF_URL_LOCATOR
PDF_TITLE_LOCATOR =liner.PDF_TITLE_LOCATOR
CLASS_TITLE = liner.CLASS_TITLE
FILE_PAGE_SELECTOR = liner.FILE_PAGE_SELECTOR
FILE_1_XPATH =liner.FILE_1_XPATH
FILE_LOCATOR =liner.FILE_LOCATOR
FILE_NAME_LOCATOR =liner.FILE_NAME_LOCATOR
FILE_DOWNLOAD_LOCATOR =liner.FILE_DOWNLOAD_LOCATOR
EXPAND_LOCATOR = liner.EXPAND_LOCATOR
EXPAND_TEXT = liner.EXPAND_TEXT
EXPAND_FALSE = liner.EXPAND_FALSE

PER_CLASS_URL_EXTERNAL_TOOLS = liner.PER_CLASS_URL_EXTERNAL_TOOLS
PER_CLASS_URL_EXTERNAL_TOOLS73 = liner.PER_CLASS_URL_EXTERNAL_TOOLS73
PER_CLASS_ALL_PAGE = liner.PER_CLASS_ALL_PAGE
PER_CLASS_ALL_PAGE_LOCATOR = liner.PER_CLASS_ALL_PAGE_LOCATOR
PER_CLASS_TITLE_LOCATOR = liner.PER_CLASS_TITLE_LOCATOR
PER_CLASS_STATUS_LOCATOR = liner.PER_CLASS_STATUS_LOCATOR
PER_CLASS_URL_LOCATOR = liner.PER_CLASS_URL_LOCATOR
PER_CLASS_DATE_CHECK =liner.PER_CLASS_DATE_CHECK
PER_CLASS_DATE_LOCATOR = liner.PER_CLASS_DATE_LOCATOR
PER_CLASS_DATE_START_LOCATOR=liner.PER_CLASS_DATE_START_LOCATOR
PER_CLASS_IS_DONE = liner.PER_CLASS_IS_DONE
USER_DASHBOARD = f'https://canvas.ssu.ac.kr/learningx/dashboard?user_login={id}&locale=ko'


class LearningX:
    def __init__(self,queue:mp.Queue):
        self.queue = queue
        try:
            self.id = os.environ.get("ID")
        except:
            self.id = input("ID : ")
        try:
            self.pw = os.environ.get("PW")
        except:
            self.pw = input("PW : " )
        self.user=None
        self.class_pickle= {}
        self.classlist = {}
        self.ssu= SSU()
        self.mainlist = {}
        self.login = None
        self.context1=None
        self.context2=None
        self.dead_thread=[]

    #? Queue 통신
    def send_message(self,message):
        self.queue.put(message)
        
    def get_classlist(self):
        """return classlist"""
        return self.classlist
    
    def checking_ID_PW(self,id,pw):
        if id!=self.id and id!="":
            self.id=id 
        if pw!=self.pw and pw!="":
            self.pw = pw
        with sync_playwright() as p:
            for browser_type in [p.chromium]:
                p.selectors.register("tag",TAG_SELECTOR)
                desktop = p.devices["Desktop Chrome"]
                browser = p.chromium.launch(channel='chrome')
                self.context1 = browser.new_context(**desktop)
                page = browser.new_page()
                try:
                    check = self.searchID_PW(page, self.id, self.pw)
                    print("login OK")
                    return True
                except:
                    return False
    def get_assigment_first(self):
        with sync_playwright() as p:
            for browser_type in [p.chromium]:
                p.selectors.register("tag",TAG_SELECTOR)
                desktop = p.devices["Desktop Chrome"]
                browser = p.chromium.launch(channel='chrome')
                context1 = browser.new_context(**desktop)
                page = browser.new_page()
                check = self.searchID_PW(page, self.id, self.pw)
                for class_name in self.classlist:
                    mainC:main_class = self.classlist[class_name]
                    assigments = mainC.get_assignment()
                    for assign in assigments:
                        self.assignment_page(check,assign)
            
    def per_process_do_first(self,p_cls):
        try:
            with sync_playwright() as p:
                for browser_type in [p.chromium]:
                    p.selectors.register("tag",TAG_SELECTOR)
                    desktop = p.devices["Desktop Chrome"]
                    browser = p.chromium.launch(channel='chrome')
                    context1 = browser.new_context(**desktop)
                    page = browser.new_page()
                    check = self.searchID_PW(page, self.id, self.pw)
                    self.get_todo(check,self.classlist[p_cls])
        except:
            self.dead_thread.append(p_cls)
            print(f"Thread Error {p_cls}")
    
    def custom_error_callback(self,error):
        print(f'Got an Error: {error}', flush=True)
    #? pdf,file,assignment
    def donwload(self,page):
        for per_class in self.classlist:
            main_class = self.classlist[per_class]
            print("MAINCLAS NAME : " ,per_class)
            have_pdf= os.scandir(f'./{main_class.title}/pdf/')
            have_pdf =set(x.name for x in have_pdf)
            pdfs = main_class.get_pdf()
            for pdf in pdfs:
                if pdf.title in have_pdf or self.clean_text(pdf.title) in have_pdf or pdf.title+".pdf" in have_pdf or self.clean_text(pdf.title+".pdf") in have_pdf:
                    print(pdf.title,'존재')
                    continue
                is_end  = self.pdf_page(page,pdf)
                if is_end==-1:
                    print(f"RETRY {pdf.title}")
                    is_end=self.pdf_page(page,pdf)
                else:
                    continue
            with open(f'./{main_class.title}/pdf/pdf.txt') as f:  
                for pdf in pdfs:
                    f.write(pdf.title+'\n')
            have_files = os.scandir(f'./{main_class.title}/files/')
            have_files = set(x.name for x  in have_files)
            files = main_class.get_file()
            for file in files:
                if file.title in have_files or self.clean_text(file.title) in have_files or file.title+".pdf" in have_files or self.clean_text(file.title+".zip") in have_pdf:
                    print(file.title,'존재')
                    continue
                is_end = self.file_page(page,file)
                if is_end==-1:
                    print(f"RETRY {file.title}")
                    is_end=self.file_page(page,file)
                else:
                    continue
            with open(f'./{main_class.title}/files/file.txt') as f:  
                for file in files:
                    f.write(file.title+'\n')
        self.send_message("end get class")
    
    def run(self,is_run=True):
        tag_selector = TAG_SELECTOR
        with sync_playwright() as p:
            for browser_type in [p.chromium]:
                p.selectors.register("tag",tag_selector)
                ##! headless or headless=False
                # browser = p.chromium.launch(channel='chrome',headless=False)
                desktop = p.devices["Desktop Chrome"]
                browser = p.chromium.launch(channel='chrome')
                self.context1 = browser.new_context(**desktop)
                page = browser.new_page()
                temping = self.searchID_PW(page, self.id, self.pw)
                #log Logins
                self.send_message("Login Access")
                self.send_message("server is ok")
                user_locator = str(temping.locator('.xn-header-member-btn-text.xn-common-title').text_content()).split("(")[0]
                self.user = user_locator
                self.send_message(f"Welcome ! : {self.user}")                
                classes = self.get_class(temping) 
                #! 맨처음 시작할때
                if not is_run:
                    page_list = []
                    for i in self.classlist:
                        page_list.append(self.searchID_PW(browser.new_page(),self.id,self.pw))

                    main_class_name_list = self.classlist.keys()
                    process_list = []
                    for i,class_name in enumerate(main_class_name_list):
                        process_list.append([threading.Thread(target=self.per_process_do_first,args=(class_name,)),class_name])
                    
                    now = time.time()
                    for start in process_list:
                        try:
                            start_t:threading.Thread = start[0]
                            start_t.start()
                            time.sleep(1) 
                        except:
                            time.sleep(1)
                            start_t.start()
                            pass
                    
                    for t in process_list:
                        t[0].join()
                    retry_thread=[]
                    for thread in self.dead_thread:
                        new_thread= threading.Thread(target=self.per_process_do_first,args=(thread,))
                        retry_thread.append(new_thread)
                    for j in retry_thread:
                        j.start()
                    for j in retry_thread:
                        j.join()
                    
                    assign = threading.Thread(target=self.get_assigment_first)
                    assign.start()
                    assign.join()
                    print("all end")
                    end = time.time()
                    print(end-now)
                    self.make_dir()
                    browser.close()
                    print("PER CLASS DOWNLOAD END..")
                    return self.show_class_dict()
                else:
                    self.donwload(page)
                browser.close()
        return 

    # ============================동영상 강의 STREAM =================================
    def stream(self):
        tag_selector =TAG_SELECTOR
        self.send_message("STREAM START")
        with sync_playwright() as p:
            for browser_type in [p.chromium]:
                p.selectors.register("tag",tag_selector)
                desktop = p.devices["Desktop Chrome"]
                browser = p.chromium.launch(channel='chrome')
                # browser = p.chromium.launch(channel='chrome',headless=False)
                self.context2 = browser.new_context(**desktop)
                page = browser.new_page()
                temping = self.searchID_PW(page, self.id, self.pw)
                self.stream_from_ssu(page)
                self.send_message("end get class")
                browser.close()
        return
    
    def check_todo_done(self,main_class:main_class,page:Page):
        page.goto(main_class.url+PER_CLASS_URL_EXTERNAL_TOOLS73)
        page.wait_for_load_state('domcontentloaded')
        page.wait_for_load_state('networkidle')
        frame= page.frame_locator('#tool_content')
        tr_locator = frame.locator('tbody').locator('tr')
        external_dict = {}
        count = tr_locator.count()
        # print(count)
        for index in range(count):
            current = tr_locator.nth(index)
            title =current.locator('.xnlaltas-table-column-title').text_content()
            attendence =current.locator('.xnlaltas-table-column-attendance_status').text_content()
            # print(title,attendence)
            external_dict[title]=attendence
        # print(external_dict)
        for cls in main_class.get_video():
            cls:todo_class
            try:
                c = external_dict[cls.title]
                pass
            except KeyError:
                print(f"KEY ERROR {cls.title}")
                self.key_error(page,cls)
                c = external_dict[cls.title]
            if c=="출석" or c=="결석":
                cls.check_done()
        return main_class
    
    def key_error(self,page:Page,todo_class:todo_class):
        page.goto(todo_class.url)
        page.wait_for_load_state('domcontentloaded')
        frame= page.frame_locator('#tool_content')
        title=frame.locator('.xnlailct-title').text_content()
        print(f"{title} <= {todo_class.title}")
        todo_class.change_title(title)
        return page
    
    def url_parse(self,course_id,item_id):
        origin = f"https://canvas.ssu.ac.kr/courses/{course_id}/modules/items/{item_id}?return_url=/courses/{course_id}/external_tools/71"
        return origin
    
    def stream_from_ssu(self,page:Page):
        print("SSU FORWARDING...")
        while 1:
            try:
                self.ssu.streaming(self.queue,page)
                self.ssu.curent_stream += 1
            except IndexError:
                self.send_message("all done")
                return 
            except Exception as e:
                print(e)
                return
    
    def searchID_PW(self, page: Page, id, pw):
        page.goto(MY_PAGE)
        get_started = page.locator('.btn_login')
        expect(get_started).to_have_text('로그인')
        get_id = page.locator(FOR_ID_ITME)
        get_pw = page.locator(FOR_PW_ITME)
        get_id.fill(id)
        get_pw.fill(pw)
        get_started.click()
        try:
            page.on("dialog", self.handle_dialog)
            page.wait_for_url(MAIN_URL)
        except Exception as e:
            pass
        return page

    def handle_dialog(self,dialog):
        print(dialog.message)
        dialog.dismiss()
        self.send_message(dialog.message)
        raise Exception
    
    def get_class(self, page: Page):
        """go to User Dash Board
            Then get main class and save to classlist
            want to main_class object find to use main class name 
        """
        page.goto(
            USER_DASHBOARD)
        page.wait_for_load_state('networkidle')
        page.inner_html('div#root')
        temp = page.get_by_text('모두 펼치기')
        temp.click()
        html = page.query_selector('//*[@id="root"]/div/div/div[2]/div[2]')
        # class_todo = page.query_selector_all('.xn-student-todo-item-container')
        class_name = page.query_selector_all('.xnscc-header-title')
        class_url = page.query_selector_all('.xnscc-header-redirect-link')
        all_class = dict()
        for index, name in enumerate(class_name):
            name.select_text()
            url = class_url[index].get_attribute('href')
            all_class[name.inner_text()] = {
                                      "url": url, "name": name.inner_text()}
            input_SSU:main_class = main_class(name.inner_text(), url, page) #title ,url ,per page
            if not name.inner_text() in self.classlist:
                self.classlist[name.inner_text()] = input_SSU
        return all_class
    
    def get_todo(self,page:Page,main_class:main_class):
        now = datetime.now()
        class_url = main_class.url
        class_name = main_class.title
        print(f"{class_name} Thread Start")
        page.goto(class_url+PER_CLASS_URL_EXTERNAL_TOOLS)
        page.wait_for_load_state('domcontentloaded')
        self.expand_c_list(page)
        # print("class MAIN NAME : ",class_name)
        per_class_all = page.frame_locator(PER_CLASS_ALL_PAGE)
        per_class_all = per_class_all.locator(PER_CLASS_ALL_PAGE_LOCATOR)
        count = per_class_all.count()
        for i in range(count):#수업안에 소클래스
            get_class = per_class_all.nth(i)
            class_status = get_class.locator(PER_CLASS_STATUS_LOCATOR)
            class_title = get_class.locator(PER_CLASS_TITLE_LOCATOR)
            class_per_url = get_class.locator(PER_CLASS_URL_LOCATOR).get_attribute('href')
            class_rest =''
            class_status = class_status.get_attribute('class')
            if "시작" in get_class.locator(PER_CLASS_DATE_CHECK).text_content() or "마감" in get_class.locator(PER_CLASS_DATE_CHECK).text_content():
                class_rest = get_class.locator(PER_CLASS_DATE_LOCATOR)
                if get_class.locator(PER_CLASS_DATE_CHECK).text_content().startswith("시작"):
                    class_rest = class_rest.locator('span').text_content()    
                    class_rest = self.time_mining(class_rest)
                    unlock= get_class.locator(PER_CLASS_DATE_START_LOCATOR).locator('span').text_content()
                    unlock = self.time_mining(unlock)
                    if now<unlock:
                        continue
                else:
                    class_rest = class_rest.locator('span').text_content()    
                    class_rest = self.time_mining(class_rest)
            main_class.add_property(class_title.text_content(),PER_URL+class_per_url,class_status,class_rest)
            # print(class_title.text_content(),PER_URL+class_per_url,class_status,class_rest)
        main_class=self.check_todo_done(main_class,page)
        for video in main_class.get_video():
            # print(video.show())
            self.ssu.add_todo_class(video)
        print(f"{class_name} Thread 종료")
    
    #class / pdf,assignment,files
    def time_mining(self,time):
        if '오후' in time:
            time = datetime.strptime(time, "%m월 %d일 오후 %H:%M")
            time = time.replace(year=2023,hour=time.hour+12)
            
        elif '오전' in time:
            time = datetime.strptime(time, "%m월 %d일 오전 %H:%M")
            time= time.replace(year=2023)
        
        return time
    
    def make_dir(self):
        for i in self.classlist:
            os.makedirs(f"./{i}", exist_ok=True)
            os.makedirs(f"./{i}/files/", exist_ok=True)
            os.makedirs(f"./{i}/pdf/", exist_ok=True)
            os.makedirs(f"./{i}/assignment/", exist_ok=True)
            self.send_message(f"{i} Checked\n.")

    def dump_frame_tree(self, frame, indent, stack=[]):
        # stack.append(indent + frame.name + '@' + frame.url)
        stack.append(frame.url)
        for child in frame.child_frames:
            self.dump_frame_tree(child, indent + "    ", stack)
            return stack

    def dump_frame_tree2(self, frame, indent, stack=[]):
        self.send_message(indent + frame.name + '@' + frame.url)
        stack.append(frame)
        for child in frame.child_frames:
            self.dump_frame_tree2(child, indent + "    ", stack)
        return stack
    
    def clean_text(self,filename):
        # Windows 파일 이름에 사용할 수 없는 문자 패턴 정의
        pattern = r'[\\\/\:\*\?\"\<\>\|]'
        result = filename.replace(" ","_")
        # 패턴과 일치하는 문자를 빈 문자열로 대체하여 반환
        result = re.sub(pattern, '', result)
        return result
    
    def unzip(self,source_file, dest_path):
        with zipfile.ZipFile(source_file, 'r') as zf:
            zipInfo = zf.infolist()
            for member in zipInfo:
                try:
                    print(member.filename.encode('cp437').decode('euc-kr', 'ignore'))
                    member.filename = member.filename.encode('cp437').decode('euc-kr', 'ignore')
                    zf.extract(member, dest_path)
                except:
                    print(source_file)
                    raise Exception('what?!')
    
    def pdf_page(self,page:Page, todo_class:todo_class):
        class_url=todo_class.url
        class_name=todo_class.main_class_name
        pdf_title = self.clean_text(todo_class.title)
        if os.path.exists(f'./{class_name}/pdf/{pdf_title}.pdf'):
            return 1
        try:
            page.goto(class_url)
            page.wait_for_load_state('networkidle')
            page.wait_for_selector(
                PDF_PAGE_SELECTOR)
            pdf_title = "None"
            pdf_url = ""
            firstframe = page.frame_locator(
                PDF_1_XPATH)
            secondframe = firstframe.frame_locator(
                PDF_2_XPATH)
            pdf_url = secondframe.locator(
                PDF_URL_LOCATOR).get_attribute('content')
            pdf_title = secondframe.locator(
                PDF_TITLE_LOCATOR).get_attribute('content')
            pdf_url = str(pdf_url).split("slides")[0]+'original.pdf'
            self.send_message("pdf_donload")
            r = requests.get(str(pdf_url), stream=True)
            pdf_title = self.clean_text(pdf_title)
            if not os.path.exists(f'./{class_name}/pdf/{pdf_title}.pdf'):
                self.send_message(f'start download {pdf_title}')
                with open(os.path.join(f'./{class_name}/pdf',f'{pdf_title}.pdf'), 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=2000):
                        fd.write(chunk)
                    self.send_message('download FINISHED')
            else:
                self.send_message(f"{pdf_title} 이 이미 있습니다.")
            return 1
        except Exception as e:
            print(e)
            self.send_message("PDF PAGE ERROR")
            todo_class.is_fail=True
            return -1
        
    
    def file_page(self, page:Page,todo_class:todo_class):
        class_url = todo_class.url
        class_name = todo_class.main_class_name
        filename = self.clean_text(todo_class.title)
        if os.path.exists(f'./{class_name}/files/{filename}'):
            return 1
        try:
            self.send_message("=============File_donwload 시작=================")
            # self.send_message(self.class_pickle[class_name][class_temp])
            # class_title.click()
            page.goto(class_url)
            page.wait_for_load_state('networkidle')
            page.wait_for_selector(
                FILE_PAGE_SELECTOR)
            pdf_title = "None"
            pdf_url = ""
            firstframe = page.frame_locator(
                FILE_PAGE_SELECTOR)
            # print("FILE_PAGE_SELECTOR OK ")
            file = firstframe.locator(FILE_LOCATOR)
            # print("file container OK")
            filename =file.locator(FILE_NAME_LOCATOR).text_content()
            filename = self.clean_text(filename)
            # print("filename OK")
            self.send_message(f"FILE : {filename} Downloading...")
            fileexpand= str(filename).split(".")[-1]
            if not os.path.exists(f'./{class_name}/files/{filename}'):
                with page.expect_download() as download_info:
                    file.locator(FILE_DOWNLOAD_LOCATOR).click()
                download = download_info.value
                download.save_as(os.path.join(f'./{class_name}/files',f'{filename}'))
                self.send_message('File download FINISHED')
            else:
                if fileexpand=='zip' and not os.path.exists(f'./{class_name}/files/{str(filename)[:-4]}'):
                    zipfile_path= f'./{class_name}/files/{filename}'
                    file_path =  f'./{class_name}/files/{filename[:-4]}'
                    os.makedirs(file_path, exist_ok=True)
                    self.unzip(zipfile_path,file_path)
                    self.send_message('FILE 압축 해제')
                self.send_message(f"{filename} 이 이미 있습니다.")
            return 1
        except Exception as e:
            todo_class.is_fail=True
            print(e)
            self.send_message("FILE_PAGE ERROR")
            return -1

    def assignment_page(self,page:Page, todo_class:todo_class):
        class_url = todo_class.url
        class_name = todo_class.main_class_name
        # print(class_name)
        title:str = todo_class.title.strip()
        title = title.strip('\n')
        if os.path.exists(f'./{class_name}/assignment/{title}.png'):
            todo_class.set_image_path(f'./{class_name}/assignment/{title}.png')
            return
        else:
            try:
                # print("make png...")
                self.send_message("=============assigment_load=================")
                page.goto(class_url)
                page.wait_for_load_state('networkidle')
                page.wait_for_selector('h1.title')
                title = page.locator('h1.title').text_content().strip().strip('\n')
                assignment_box = page.locator('#assignment_show')
                assignment = assignment_box.locator(".description")
                assignment.screenshot(path=os.path.join(f'./{class_name}/assignment',f'{title}.png'))
                path = f'./{class_name}/assignment/{title}.png'
                todo_class.set_image_path(path)
                # print(path)
                return 
            except Exception as e:
                todo_class.is_fail=True
                print(e)
                self.send_message("FILE_PAGE ERROR")
                return -1

    def notice_page(self,page:Page):
        #! 추후 작업 예정
        return 1

    def expand_c_list(self, page: Page):
        page.wait_for_load_state('networkidle')
        frame = page.frame_locator(EXPAND_LOCATOR)
        try:
            check = frame.get_by_text(EXPAND_TEXT).text_content()
            if EXPAND_FALSE in str(check):
                frame.get_by_text(EXPAND_FALSE).click()
            else:
                return
        except Exception as e:
            print(e)
    
    def synch_todo_url(self,page:Page,class_url,class_name):
        try:
            print("sync start..")
            page.goto(class_url+PER_CLASS_URL_EXTERNAL_TOOLS)
            page.wait_for_load_state('domcontentloaded')
            page.wait_for_load_state('networkidle')
            self.expand_c_list(page)
            #? page 확장
            print("class MAIN NAME : ",class_name)
            per_class_all = page.frame_locator(PER_CLASS_ALL_PAGE)
            per_class_all = per_class_all.locator(PER_CLASS_ALL_PAGE_LOCATOR)#queryselect all
            count = per_class_all.count()
            print("수업 개수 : ",count)
            # class_main:main_class = self.classlist[class_name]
            for i in range(count):
                get_class = per_class_all.nth(i)
                class_status = get_class.locator(PER_CLASS_STATUS_LOCATOR)
                class_title = get_class.locator(PER_CLASS_TITLE_LOCATOR)
                class_title = class_title.text_content()   
                class_per_url = get_class.locator(PER_CLASS_URL_LOCATOR).get_attribute('href')
                class_status = class_status.get_attribute('class')
                if "everlec" in class_status:
                    check = self.ssu.sync_main_2_todo(class_title,class_per_url)
                    if check:
                        print(f"async..{class_title}")                    
            print("sync end")
        except Exception as e:
            print(e)


    #메인 서버에서 접속불가시 우회접속==========================
    
    def main_server_shut_down(self, p: Page,classes_url:list):
        get_started = p.get_by_role("link", name="모든 과목")
        self.send_message(get_started)
        expect(get_started).to_have_attribute("href", "/courses/")
        for class_url in classes_url:
            self.per_class_get_todo(p, class_url)

    def per_class_get_todo(self, p: Page,class_url):
        p.goto(p.url+class_url+PER_CLASS_URL_EXTERNAL_TOOLS)
        p.wait_for_load_state('networkidle')
        frame = p.frame_locator('.tool_launch').get_by_text('모든 주차')
        frame.click()
    #=======================================================================
    
    def show_class_dict(self):
        classes={}
        for i in self.classlist:
            classes[self.classlist[i].title]=self.classlist[i].url
        return classes

    def get_todo_2_dict(self):
        return self.ssu.get_todo()

