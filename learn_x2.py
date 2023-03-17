#-*- coding: utf-8 -*-
import re
from playwright.sync_api import Page, expect, sync_playwright , Browser
import playwright.sync_api as pl
import os
import dotenv
from multiprocessing import Queue, Process,Pool
import multiprocessing as mp
import time
import requests
import pickle
import zipfile
import threading
from datetime import datetime
from urllib.parse import urlsplit, parse_qsl
from line import Local

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

tododict = {'video': 1, 'assignment': 2}
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

    #? Queue 통신
    def send_message(self,message):
        # self.lock.acquire(block=True)
        # print(f"put message in to :{message}")
        self.queue.put(message)
        # self.lock.release()
    def get_classlist(self):
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
    #? pdf,file,assignment
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
                classes = self.get_class(temping) #main class get & save
                #! 맨처음 시작할때
                if not is_run:
                    print("PER CLASS ALL DOWNLOADING >>>>>..")
                    self.get_todo(page)
                    self.make_dir()
                    browser.close()
                    print("PER CLASS DOWNLOAD END..")
                    return self.show_class_dict()

                self.index = 0
                self.before = 0
                self.checking_set= set()
                main_key = list(self.classlist.keys())
                self.send_message(f"수업 개수 :  {len(main_key)}")
                for per_class in self.classlist:
                    main_class = self.classlist[per_class]
                    print(per_class)
                    print("PDF FIND >>>>")
                    # main_class.show()
                    pdfs = main_class.get_pdf()
                    files = main_class.get_file()
                    for pdf in pdfs:
                        is_end  = self.pdf_page(page,pdf)
                        if is_end==-1:
                            print("RETRY {pdf.title}")
                            is_end=self.pdf_page(page,pdf)
                        else:
                            continue
                    # print("FILE FIND >>>>")
                    for file in files:
                        is_end = self.file_page(page,file)
                        if is_end==-1:
                            print("RETRY {file.title}")
                            is_end=self.file_page(page,file)
                        else:
                            continue
                self.send_message("end get class")
                browser.close()
        return 
    # ============================동영상 강의 자동재생 =================================
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
                #----------------
                # i = self.get_class(page)
                # self.get_todo(page)
                #--------------------------------
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
        print(count)
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
            print(e)
            pass
        return page

    def handle_dialog(self,dialog):
        print(dialog.message)
        dialog.dismiss()
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
        # self.make_dir()
        return all_class
    
    def get_todo(self,page:Page):
        now = datetime.now()
        for p_cls in self.classlist: #각 수업의 
            class_url = self.classlist[p_cls].url
            class_name = p_cls
            page.goto(class_url+PER_CLASS_URL_EXTERNAL_TOOLS)
            page.wait_for_load_state('domcontentloaded')
            # page.wait_for_load_state('networkidle')
            self.expand_c_list(page)
            print("class MAIN NAME : ",class_name)
            per_class_all = page.frame_locator(PER_CLASS_ALL_PAGE)
            per_class_all = per_class_all.locator(PER_CLASS_ALL_PAGE_LOCATOR)
            count = per_class_all.count()
            class_main:main_class = self.classlist[class_name]
            for i in range(count):#수업안에 소클래스
                get_class = per_class_all.nth(i)
                class_status = get_class.locator(PER_CLASS_STATUS_LOCATOR)
                class_title = get_class.locator(PER_CLASS_TITLE_LOCATOR)
                class_per_url = get_class.locator(PER_CLASS_URL_LOCATOR).get_attribute('href')
                class_rest =''
                class_status = class_status.get_attribute('class')
                if get_class.locator(PER_CLASS_DATE_CHECK).text_content()!="":
                    class_rest = get_class.locator(PER_CLASS_DATE_LOCATOR)
                    if get_class.locator(PER_CLASS_DATE_CHECK).text_content().startswith("시작"):
                        class_rest = class_rest.locator('span').text_content()    
                        print(class_rest)
                        class_rest = self.time_mining(class_rest)
                        print(class_rest)
                        unlock= get_class.locator(PER_CLASS_DATE_START_LOCATOR).locator('span').text_content()
                        unlock = self.time_mining(unlock)
                        if now<unlock:
                            continue
                    else:
                        class_rest = class_rest.locator('span').text_content()    
                        print(class_rest)
                        class_rest = self.time_mining(class_rest)
                        print(class_rest)
                # print(class_main.url)
                class_main.add_property(class_title.text_content(),PER_URL+class_per_url,class_status,class_rest)
                print(class_title.text_content(),PER_URL+class_per_url,class_status,class_rest)
            
        for p_cls in self.classlist:
            print(p_cls)
            class_url = self.classlist[p_cls].url
            class_name = p_cls
            class_main:main_class = self.classlist[class_name]
            class_main=self.check_todo_done(class_main,page)
            for video in class_main.get_video():
                print(video.show())
                self.ssu.add_todo_class(video)
        # self.ssu.showing_main()
    
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
            os.makedirs(f'./{i}', exist_ok=True)
            os.makedirs(f"./{i}/files", exist_ok=True)
            os.makedirs(f"./{i}/pdf", exist_ok=True)
            os.makedirs(f"./{i}/assignment", exist_ok=True)
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
        print(class_url)
        print(class_name)
        try:
            # class_title.click()
            page.goto(class_url)
            page.wait_for_load_state('networkidle')
            page.wait_for_selector(
                PDF_PAGE_SELECTOR)
            # print("PDF_PAGE_SELECTOR")
            pdf_title = "None"
            pdf_url = ""
            firstframe = page.frame_locator(
                PDF_1_XPATH)
            # print("PDF_1_XPATH OK")
            secondframe = firstframe.frame_locator(
                PDF_2_XPATH)
            # print("PDF_2_XPATH OK ")
            pdf_url = secondframe.locator(
                PDF_URL_LOCATOR).get_attribute('content')
            pdf_title = secondframe.locator(
                PDF_TITLE_LOCATOR).get_attribute('content')
            pdf_url = str(pdf_url).split("slides")[0]+'original.pdf'
            self.send_message("pdf_donload")
            r = requests.get(str(pdf_url), stream=True)
            pdf_title = self.clean_text(pdf_title)
            print(pdf_title)
            if not os.path.exists(f'./{class_name}/pdf/{pdf_title}.pdf'):
                self.send_message(f'start download {pdf_title}')
                with open(f'./{class_name}/pdf/{pdf_title}.pdf', 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=2000):
                        fd.write(chunk)
                    self.send_message('download FINISHED')
            return 1
        except Exception as e:
            print(e)
            self.send_message("PDF PAGE ERROR")
            todo_class.is_fail=True
            return -1
        
    
    def file_page(self, page:Page,todo_class:todo_class):
        class_url = todo_class.url
        class_name = todo_class.main_class_name
        
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
            print("FILE_PAGE_SELECTOR OK ")
            file = firstframe.locator(FILE_LOCATOR)
            print("file container OK")
            filename =file.locator(FILE_NAME_LOCATOR).text_content()
            filename = self.clean_text(filename)
            print("filename OK")
            self.send_message(f"FILE : {filename} Downloading...")
            fileexpand= str(filename).split(".")[-1]
            if not os.path.exists(f'./{class_name}/files/{filename}'):
                with page.expect_download() as download_info:
                    file.locator(FILE_DOWNLOAD_LOCATOR).click()
                download = download_info.value
                download.save_as(os.path.join(f'./{class_name}/files/{filename}'))
                self.send_message('File download FINISHED')
            else:
                if fileexpand=='zip' and not os.path.exists(f'./{class_name}/files/{str(filename)[:-4]}'):
                    zipfile_path= f'./{class_name}/files/{filename}'
                    file_path =  f'./{class_name}/files/'
                    self.unzip(zipfile_path,file_path)
                    self.send_message('FILE 압축 해제')
                self.send_message(f"{filename} 이 이미 있습니다.")
            return 1
        except Exception as e:
            todo_class.is_fail=True
            print(e)
            self.send_message("FILE_PAGE ERROR")
            return -1

    #! 미완성
    def assignment_page(self, class_name:str, page:Page,class_title:pl.Locator):
            class_title.click()
            page.wait_for_load_state('networkidle')
            firstframe = page.frame_locator('iframe#tool_content')
            assignment = firstframe.locator(".xn-unit-container")
            assignment.screenshot(path=f'./{class_name}/assignment/{class_title}.png')
            self.send_message("screenshot!")
            try:
                href = firstframe.locator('href')
                href_count = href.count()
            except:
                href = 0
                href_count=0
            self.send_message(href_count)
            if href_count>0:
                assignment_file = firstframe.locator('.instructure_file_link.instructure_scribd_file')
                self.send_message(f'Assignment Download Checking : {assignment_file.get_attribute("title")}')
                with page.expect_download() as download_info:
                    assignment_file.click()
                download = download_info.value
                download.save_as(os.path.join(f'./{class_name}/assignment/{assignment_file.get_attribute("title")}'))
                self.send_message('Assignment download FINISHED')
            else:
                self.send_message("Assignment no file")
            return 

    def notice_page(self,page:Page):
        #! 추후 작업 예정
        return 1

    def expand_c_list(self, page: Page):
        page.wait_for_load_state('networkidle')
        frame = page.frame_locator(EXPAND_LOCATOR)
        try:
            check = frame.get_by_text(EXPAND_TEXT).text_content()
            print(str(check))
            if EXPAND_FALSE in str(check):
                frame.get_by_text(EXPAND_FALSE).click()
            else:
                pass
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


    #각 class tool 73안에서 일어나는 일
    def per_class_download(self, page: Page,class_name:str,class_url:str,class_index:int,checking_set:set):
        pass
        # page.goto(class_url+PER_CLASS_URL_EXTERNAL_TOOLS)
        # page.wait_for_load_state('domcontentloaded')
        # page.wait_for_load_state('networkidle')
        # self.expand_c_list(page)
        # #? page 확장
        # print("class MAIN NAME : ",class_name)
        # per_class_all = page.frame_locator(PER_CLASS_ALL_PAGE)
        # per_class_all = per_class_all.locator(PER_CLASS_ALL_PAGE_LOCATOR)#queryselect all
        # count = per_class_all.count()
        # #? recursive 다 checking 시
        # if count==len(checking_set):
        #     self.send_message(f"count와 checking_set : {count}, {len(checking_set)}")
        #     return True
        # if class_index == 0 and class_name not in self.class_pickle:
        #     class_main:main_class = self.classlist[class_name]
        #     class_per_dict = dict()
        #     class_per_dict['name'] = class_name
        #     class_per_dict['url'] = class_url
        #     main_per_class = main_class(class_name, class_url+PER_CLASS_URL_EXTERNAL_TOOLS, page)
        #     self.class_pickle[class_name]=dict()
        #     for i in range(count):
        #         get_class = per_class_all.nth(i)
        #         class_status = get_class.locator(PER_CLASS_STATUS_LOCATOR)
        #         class_title = get_class.locator(PER_CLASS_TITLE_LOCATOR)
        #         class_per_url = get_class.locator(PER_CLASS_URL_LOCATOR).get_attribute('href')
        #         class_status = class_status.get_attribute('class')
        #         class_main.add_property(class_title.text_content(),class_per_url,class_status)
        #         self.class_pickle[class_name][str(class_title.text_content())]=False
        #     self.send_message("MAIN CLASS GET ")
        #     # for j in self.classlist:
        #     #     self.classlist[j].show()
        # if class_index == count:
        #     self.send_message(f"{class_name} 끝! 다음으로 넘어갑니다.")
        #     return True
        # try:
        #     self.send_message("하위 항목 살피기 ...")
        #     while class_index < count:
        #         class_ = per_class_all.nth(class_index)
        #         self.send_message('===========================================')
        #         self.send_message(f"현재 index : {class_index}")
        #         self.send_message(f"총 index : {count}")
        #         class_status = class_.locator(PER_CLASS_STATUS_LOCATOR)
        #         class_title = class_.locator(PER_CLASS_TITLE_LOCATOR)
        #         # self.send_message(type(class_title))
        #         class_status = class_status.get_attribute('class')
        #         self.send_message(class_title.text_content())
        #         self.send_message(class_status)
        #         if class_title.text_content() in checking_set:
        #             self.send_message(f"{class_title.text_content()} 을 건너뜁니다.")
        #             class_index += 1
        #             continue
        #         else:
        #             checking_set.add(class_title.text_content())
        #             class_status = str(class_status).split()
        #             try:
        #                 class_temp = str(class_title.text_content())
        #                 if "pdf" in class_status and not os.path.exists(f'./{class_name}/pdf/{class_temp}.pdf'):
        #                     self.pdf_page(class_name, page, class_title,class_temp,self.class_pickle)
        #                     class_index = self.per_class_download(page, class_name, class_url,class_index,checking_set)
        #                     page.wait_for_load_state('networkidle')
        #                 elif "file" in class_status and not os.path.isfile(f'./{class_name}/files/{class_temp}'):
        #                     self.file_page(class_name, page, class_title,class_temp, self.class_pickle)
        #                     class_index = self.per_class_download(page, class_name, class_url,class_index,checking_set)
        #                     page.wait_for_load_state('domcontentloaded')
        #                 else:
        #                     self.class_pickle[class_name][class_temp]=True
        #                 # elif "assignment" in class_status and not os.path.exists(f'./{class_name}/assignment/{class_title.text_content()}'):
        #                 #     self.assignment_page(class_name, page, class_title)
        #                 #     class_index = self.per_class_download(page, class_name, class_url,class_index+1,checking_set)
        #                 #     page.wait_for_load_state('domcontentloaded')
        #                 if class_index == True and type(class_index) is bool:
        #                     return True
        #                 if class_index>=count:
        #                     return True
        #             except:
        #                 self.send_message(f"{class_title.text_content()} : {class_index} : ERROR")
        #                 # self.classlist[class_name].class_list_error.append(class_index)
        #             class_index+=1
        #             self.send_message("=====================end===================")
        # except:
        #     self.send_message(f"{class_name} : : {class_index} : ERROR")
        #     return class_index
        # return True


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

if __name__ == '__main__':
    b = Queue()
    # a = LearningX(b).run(True)
    a = LearningX(b).run(False)
    a.run(True)
        
    # def get_class_todo_class(self,page: Page, start_todo_class=False):
    #     print("def : get class todo class")
    #     page.goto(
    #         USER_DASHBOARD)
    #     page.wait_for_load_state('networkidle')
    #     page.inner_html(GET_CLASS_TODO_CLASS_1_FRAME)
    #     temp = page.get_by_text('모두 펼치기')
    #     temp.click()
    #     page.screenshot(path='start.png')
    #     html = page.locator('xpath=//*[@id="root"]/div/div/div[2]/div[2]')
    #     todo_class_list = html.locator(
    #     '.xn-student-todo-item-container')
    #     main_class_list = html.locator('.xnscc-header-title')
    #     count = todo_class_list.count()
    #     if count >= 1:
    #         for i in range(count):
    #             main_class_name = main_class_list.nth(i).text_content()
    #             print(main_class_name+"\n")
    #             class_status = todo_class_list.nth(i).locator(
    #                 '.xnsti-left-icon').get_attribute('class')
    #             class_title = todo_class_list.nth(i).locator('.xnsti-left-title')
    #             class_rest = todo_class_list.nth(i).locator(
    #                 '.xnsti-right-dday-text').text_content()
    #             class_url = class_title.get_attribute('href')
    #             query_string = urlsplit(class_url).query
    #             parsed = dict(parse_qsl(query_string))
    #             class_url = class_url.split('/')
    #             class_id = class_url[6]
    #             print(parsed)
    #             item_id =  parsed['component_info'].split(":")[1][:-1]
    #             class_url = self.url_parse(class_id,item_id)
    #             class_title = class_title.text_content()
    #             self.ssu.add_todo_class(todo_class(class_title, class_url, class_rest, class_status, page,main_class_name))
    
    #     if start_todo_class:
    #         print("SSU FORWARDING...")
    #         while 1:
    #             try:
    #                 self.ssu.streaming(self.queue)
    #                 self.ssu.curent_stream += 1
    #             except IndexError:
    #                 self.send_message("all done")
    #                 return 1,1
    #             except Exception as e:
    #                 print(e)
    #                 return 1,1
    
    #         class_name = page.query_selector_all('.xnscc-header-title')
    #         class_url = page.query_selector_all('.xnscc-header-redirect-link')
    #         all_class = dict()
    #         for index, name in enumerate(class_name):
    #             name.select_text()
    #             url = class_url[index].get_attribute('href')
    #             class_url[index]
    #             all_class[name.inner_text()] = {"url": url}
    #         return page, all_class
    #     else:
    #         return 1,1