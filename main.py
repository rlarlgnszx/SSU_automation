#-*- coding: utf-8 -*-
import re
from playwright.sync_api import Page, expect, sync_playwright
import playwright.sync_api as pl
import os
import dotenv
from multiprocessing import Process ,Pool
import multiprocessing as mp
import time
import requests
import asyncio
import pickle
import zipfile

#=====================================================
from ssu import todo_class, SSU, main_class
from bs4 import BeautifulSoup as bs
#===================================================
dotenv.load_dotenv()
pw = os.environ.get("PW")
tododict = {'video': 1, 'assignment': 2}
class LearningX:
    def __init__(self):
        try:
            self.id = os.environ.get("ID")
        except:
            self.id = input("ID :")
        try:
            self.pw = os.environ.get("PW")
        except:
            self.pw = input("PW :")
        self.user=None
        self.class_pickle= dict()
        self.classlist = dict()
        self.ssu= SSU
        
        # self.stream_ = Process(target=self.stream)
        # self.pdf = Process(target= self.run)

    def run(self):
        tag_selector = """
        {
            // Returns the first element matching given selector in the root's subtree.
            query(root, selector) {
                return root.querySelector(selector);
            },
            // Returns all elements matching given selector in the root's subtree.
            queryAll(root, selector) {
                return Array.from(root.querySelectorAll(selector));
            }
        }"""
        with sync_playwright() as p:
            for browser_type in [p.chromium]:
                p.selectors.register("tag",tag_selector)
                browser = p.chromium.launch(channel='chrome')
                desktop = p.devices["Desktop Chrome"]
                context = browser.new_context(**desktop)
                # pdf_context = browser.new_context()
                page = browser.new_page()
                temping = self.searchID_PW(page, self.id, self.pw)
                print("start get class")
                print("server is ok")
                user_locator = str(temping.locator('.xn-header-member-btn-text.xn-common-title').text_content()).split("(")[0]
                self.user = user_locator
                print(f"Welcome ! : {self.user}")
                classes = self.get_class(temping, self.id)
                self.index = 0
                self.before = 0
                self.checking_set= set()
                main_key = list(self.classlist.keys())
                print("수업 개수 : " ,len(main_key))
                while self.index < len(main_key):
                    try:
                        # print(f'{self.classlist[main_key[self.index]].title} 를 Checking 중....')
                        print("처음 상태  :" , self.before)
                        if self.before==True and type(self.before) is bool:
                            print(f'END | {self.classlist[main_key[self.index]].title}  | END\n')
                            self.before=0
                        else:
                            while self.before!=True and type(self.before) is int:
                                print(f'{self.classlist[main_key[self.index]].title} 를 탐색중...')
                                print(f"완료 상태 . : {self.before}")
                                self.before=self.per_class_download(page, self.classlist[main_key[self.index]].title, self.classlist[main_key[self.index]].url , self.before,self.checking_set)
                                print(f"#####가장 큰 바깥쪽 RECURSIVE 상태 :{self.before} ")
                                if self.before==True and type(self.before) is bool:
                                    # True 일 경우 data 저장 =====================
                                    # checkin_final = self.class_pickle[main_key[self.index].title].keys()
                                    # for check in checkin_final:
                                    #     if not self.class_pickle[main_key[self.index].title][check]:
                                    #         print(f'{check}가 남아있습니다...')
                                    # with open(f'{main_key[self.index].title}.pickle', 'wb') as f:
                                    #     pickle.dump(self.class_pickle[main_key[self.index].title], f)
                                    print(f'END | {self.classlist[main_key[self.index]].title}  | END\n')
                                    self.before=0
                                    break
                    except:
                        print(f"{self.classlist[main_key[self.index]].title}를 완료하지 못했습니다..")
                        time.sleep(5)
                        continue
                    self.index += 1
                # except: 서버다운될경우 우회하는 경로 만들거임
                  # temping.goto('https://canvas.ssu.ac.kr')
                  # temping.wait_for_load_state('networkidle')
                  # new_class_url=[]
                  # class_url=temping.query_selector_all('.fOyUs_bGBk .fbyHH_bGBk .fbyHH_bSMN')
                  # for classes in class_url:
                  #     new_class_url.append(classes.get_attribute('href'))
                  # class_url = new_class_url[1:-1]
                  # main_server_shut_down(temping,class_url)
                print("end get class")
                browser.close()
        return
    # ============================동영상 강의 자동재생 =================================
    def stream(self):
        tag_selector = """
        {
            // Returns the first element matching given selector in the root's subtree.
            query(root, selector) {
                return root.querySelector(selector);
            },
            // Returns all elements matching given selector in the root's subtree.
            queryAll(root, selector) {
                return Array.from(root.querySelectorAll(selector));
            }
        }"""
        print("STREAM START")
        with sync_playwright() as p:
            for browser_type in [p.chromium]:
                p.selectors.register("tag",tag_selector)
                browser = p.chromium.launch(channel='chrome')
                desktop = p.devices["Desktop Chrome"]
                context = browser.new_context(**desktop)
                page = browser.new_page()
                temping = self.searchID_PW(page, self.id, self.pw)
                page, classes = self.get_class_todo_class(temping, self.id)
                print("end get class")
                browser.close()
    # def stream_start(self):
    #     self.stream_.start()
    #     self.stream_.join()
    # def pdf_download_start(self):
    #     self.pdf.start()
    #     self.pdf.join()
        return
    def get_class_todo_class(self,page: Page, id):
        page.goto(
            f'https://canvas.ssu.ac.kr/learningx/dashboard?user_login={id}&locale=ko')
        page.wait_for_load_state('networkidle')
        page.inner_html('div#root')
        temp = page.get_by_text('모두 펼치기')
        temp.click()
        page.screenshot(path='hee.png')
        html = page.locator('xpath=//*[@id="root"]/div/div/div[2]/div[2]')
        todo_class_list = html.locator(
        '.xn-student-todo-item-container')
        count = todo_class_list.count()
        if count >= 1:
            for i in range(count):
                class_status = todo_class_list.nth(i).locator(
                    '.xnsti-left-icon').get_attribute('class')
                class_title = todo_class_list.nth(i).locator('.xnsti-left-title')
                class_rest = todo_class_list.nth(i).locator(
                    '.xnsti-right-dday-text').text_content()
                class_url = class_title.get_attribute('href')
                
                class_title = class_title.text_content()
                self.ssu(todo_class(class_title, class_url, class_rest, class_status, page))
        # SSU.showing_todo()
        while 1:
            try:
                SSU.streaming()
                SSU.current_stream += 1
            except IndexError :
                print("all done")
                raise 

        new_class_dict = dict()
        # class_todo = page.query_selector_all('.xn-student-todo-item-container')
        class_name = page.query_selector_all('.xnscc-header-title')
        class_url = page.query_selector_all('.xnscc-header-redirect-link')
        all_class = dict()
        for index, name in enumerate(class_name):
            name.select_text()
            url = class_url[index].get_attribute('href')
            class_url[index]
            all_class[name.inner_text()] = {"url": url}
        new_dict = dict()
        return page, all_class

    def searchID_PW(self, page: Page, id, pw):
        page.goto('https://class.ssu.ac.kr/mypage')
        get_started = page.locator('.btn_login')
        expect(get_started).to_have_text('로그인')
        get_id = page.locator('#userid')
        get_pw = page.locator('#pwd')
        get_id.fill(id)
        get_pw.fill(pw)
        get_started.click()
        page.wait_for_url('https://class.ssu.ac.kr/')
        return page

    def get_class(self, page: Page, id):
        page.goto(
            f'https://canvas.ssu.ac.kr/learningx/dashboard?user_login={id}&locale=ko')
        page.wait_for_load_state('networkidle')
        page.inner_html('div#root')
        temp = page.get_by_text('모두 펼치기')
        temp.click()
        # page.screenshot(path='hee.png')
        html = page.query_selector('//*[@id="root"]/div/div/div[2]/div[2]')

        class_todo = page.query_selector_all('.xn-student-todo-item-container')
        class_name = page.query_selector_all('.xnscc-header-title')
        class_url = page.query_selector_all('.xnscc-header-redirect-link')
        all_class = dict()
        
        for index, name in enumerate(class_name):
            name.select_text()
            url = class_url[index].get_attribute('href')
            # class_url[s]
            
            all_class[name.inner_text()] = {
                                      "url": url, "name": name.inner_text()}
            input_SSU = main_class(name.inner_text(), url, page)
            self.classlist[name.inner_text()] = input_SSU
        self.make_dir()
        return all_class


    def make_dir(self):
        self.show_class()
        for i in self.classlist:
            os.makedirs(f'./{i}', exist_ok=True)
            os.makedirs(f"./{i}/files", exist_ok=True)
            os.makedirs(f"./{i}/pdf", exist_ok=True)
            os.makedirs(f"./{i}/assignment", exist_ok=True)

    def dump_frame_tree(self, frame, indent, stack=[]):
        # stack.append(indent + frame.name + '@' + frame.url)
        stack.append(frame.url)
        for child in frame.child_frames:
            self.dump_frame_tree(child, indent + "    ", stack)
            return stack

    def dump_frame_tree2(self, frame, indent, stack=[]):
        print(indent + frame.name + '@' + frame.url)
        stack.append(frame)
        for child in frame.child_frames:
            self.dump_frame_tree2(child, indent + "    ", stack)

        return stack

    def pdf_page(self, class_name, page:Page,class_title:pl.Locator,class_temp:str,class_pickle):
        try:
            class_title.click()
            page.wait_for_load_state('networkidle')
            page.wait_for_selector(
                'xpath=/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/iframe')
            pdf_title = "None"
            pdf_url = ""
            firstframe = page.frame_locator(
                'xpath=/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/iframe')
            secondframe = firstframe.frame_locator(
                'xpath=/html/body/div/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/iframe')
            thirdframe = secondframe.frame_locator('xpath=/html/body/div/iframe')
            pdf_url = thirdframe.locator(
                'meta[property="og:image"]').get_attribute('content')
            pdf_title = thirdframe.locator(
                'meta[property="og:title"]').get_attribute('content')

            pdf_url = str(pdf_url).split("slides")[0]+'original.pdf'
            print("pdf_donload")
            r = requests.get(str(pdf_url), stream=True)
            if not os.path.exists(f'./{class_name}/pdf/{pdf_title}.pdf'):
                print(f'start download {pdf_title}')
                with open(f'./{class_name}/pdf/{pdf_title}.pdf', 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=2000):
                        fd.write(chunk)
                    print('download FINISHED')
            self.class_pickle[class_name][class_temp]=True
        except:
            print("PDF PAGE ERROR")
        return page

    def file_page(self, class_name:str, page:Page,class_title:pl.Locator,class_temp:str,class_pickle):
        try:
            print("File_donwload 시작..")
            print(self.class_pickle[class_name][class_temp])
            class_title.click()
            page.wait_for_load_state('networkidle')
            page.wait_for_selector(
                'xpath=/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/iframe')
            pdf_title = "None"
            pdf_url = ""
            firstframe = page.frame_locator(
                'xpath=/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/iframe')
            file = firstframe.locator(".xnfc-file-container")
            filename =file.locator('.xnfc-file-name').text_content()
            print(f"FILE : {filename} Downloading...")
            fileexpand= str(filename).split(".")[-1]
            if not os.path.exists(f'./{class_name}/files/{filename}'):
                with page.expect_download() as download_info:
                    file.locator('.xnfc-download-icon').click()
                download = download_info.value
                download.save_as(os.path.join(f'./{class_name}/files/{filename}'))
                print('File download FINISHED')
            else:
                if fileexpand=='zip' and not os.path.exists(f'./{class_name}/files/{str(filename)[:-4]}'):
                    with zipfile.ZipFile(f'./{class_name}/files/{filename}', 'r') as zip_ref:
                        zip_ref.extractall(f'./{class_name}/files/')
                        print('FILE 압축 해제')
                print(f"{filename} 이 이미 있습니다.")
            self.class_pickle[class_name][class_temp]=True
        except:
            print("FILE_PAGE ERROR")
        return page
    def assignment_page(self, class_name:str, page:Page,class_title:pl.Locator):
            class_title.click()
            page.wait_for_load_state('networkidle')
            # page.wait_for_selector(
            #     'xpath=/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/iframe')
            firstframe = page.frame_locator('iframe#tool_content')
            assignment = firstframe.locator(".xn-unit-container")
            assignment.screenshot(path=f'./{class_name}/assignment/{class_title}.png')
            print("screenshot!")
            try:
                href = firstframe.locator('href')
                href_count = href.count()
            except:
                href = 0
                href_count=0
            print(href_count)
            if href_count>0:
                assignment_file = firstframe.locator('.instructure_file_link.instructure_scribd_file')
                print(f'Assignment Download Checking : {assignment_file.get_attribute("title")}')
                with page.expect_download() as download_info:
                    assignment_file.click()
                download = download_info.value
                download.save_as(os.path.join(f'./{class_name}/assignment/{assignment_file.get_attribute("title")}'))
                print('Assignment download FINISHED')
            else:
                print("Assignment no file")
            return 

    def notice_page(self,page:Page):
        #! 추후 작업 예정
        return 1

    def expand_c_list(self, page: Page):
        page.wait_for_load_state('networkidle')
        
        print("expanded c_list start")
        frame = page.frame_locator('iframe#tool_content')
        try:
            check = frame.get_by_text('모든 주차').text_content()
            if '모든 주차 펴기' in str(check):
                frame.get_by_text('모든 주차 펴기').click()
                print("모든 주차 보이기 SUCCESS")
            else:
                print("주차 열려있음")
        except:
            print("class 보이기 실패 CLICK")
            time.sleep(5)
        print("expand_c_list end")

    def per_class_download(self, page: Page,class_name:str,class_url:str,class_index:int,checking_set:set):
        
        page.goto(class_url+'/external_tools/2')
        page.wait_for_load_state('domcontentloaded')
        page.wait_for_load_state('networkidle')
        self.expand_c_list(page)

        per_class_all = page.frame_locator("#tool_content")
        per_class_all = per_class_all.locator('.xncb-component-wrapper')#queryselect all
        count = per_class_all.count()
        
        if count==len(checking_set):
            print(f"count와 checking_set : {count}, {len(checking_set)}")
            return True
        if class_index == 0 and class_name not in self.class_pickle:
            class_per_dict = dict()
            class_per_dict['name'] = class_name
            class_per_dict['url'] = class_url
            main_per_class = main_class(class_name, class_url+'/external_tools/2', page)
            self.class_pickle[class_name]=dict()
            for i in range(count):
                get_class = per_class_all.nth(i)
                class_title = get_class.locator('.xncb-component-title')
                self.class_pickle[class_name][str(class_title.text_content())]=False
            print("MAIN CLASS GET ")
        # if count==self.class_pickle[class_name].values().count(True):
            # return True
        # per_class_all = page.frame_locator("#tool_content")
        # per_class_all = per_class_all.locator('.xncb-component-wrapper')#queryselect all
        # count = per_class_all.count()
        
        # print(count)
        if class_index == count:
            print(f"{class_name} 끝! 다음으로 넘어갑니다.")
            return True
        try:
            print("하위 항목 살피기 ...")
            while class_index < count:
                # if class_index in checking_set:
                #     class_index +=1
                #     print("존재..!")
                #     continue
                class_ = per_class_all.nth(class_index)
                print('===========================================')
                print(f"현재 index : {class_index}")
                print(f"총 index : {count}")
                class_status = class_.locator('.xncb-component-icon')
                class_title = class_.locator('.xncb-component-title')
                # print(type(class_title))
                class_status = class_status.get_attribute('class')
                print(class_title.text_content())
                print(class_status)
                if class_title.text_content() in checking_set:
                    print(f"{class_title.text_content()} 을 건너뜁니다.")
                    class_index += 1
                    continue
                else:
                    checking_set.add(class_title.text_content())
                    class_status = str(class_status).split()
                    try:
                        class_temp = str(class_title.text_content())
                        if "pdf" in class_status and not os.path.exists(f'./{class_name}/pdf/{class_temp}.pdf'):
                            self.pdf_page(class_name, page, class_title,class_temp,self.class_pickle)
                            class_index = self.per_class_download(page, class_name, class_url,class_index,checking_set)
                            page.wait_for_load_state('domcontentloaded')
                        elif "file" in class_status and not os.path.isfile(f'./{class_name}/files/{class_temp}'):
                            self.file_page(class_name, page, class_title,class_temp, self.class_pickle)
                            class_index = self.per_class_download(page, class_name, class_url,class_index,checking_set)
                            page.wait_for_load_state('domcontentloaded')
                        else:
                            self.class_pickle[class_name][class_temp]=True
                        # elif "assignment" in class_status and not os.path.exists(f'./{class_name}/assignment/{class_title.text_content()}'):
                        #     self.assignment_page(class_name, page, class_title)
                        #     class_index = self.per_class_download(page, class_name, class_url,class_index+1,checking_set)
                        #     page.wait_for_load_state('domcontentloaded')
                        if class_index == True and type(class_index) is bool:
                            return True
                        if class_index>=count:
                            return True
                    except:
                        print(f"{class_title.text_content()} : {class_index} : ERROR")
                        # self.classlist[class_name].class_list_error.append(class_index)
                    class_index+=1
                    print("=====================end===================")
        except:
            print(f"{class_name} : : {class_index} : ERROR")
            return class_index
        return True


    def main_server_shut_down(self, p: Page,classes_url:list):
        get_started = p.get_by_role("link", name="모든 과목")
        print(get_started)
        expect(get_started).to_have_attribute("href", "/courses/")
        for class_url in classes_url:
            self.per_class_get_todo(p, class_url)

    def per_class_get_todo(self, p: Page,class_url):
        p.goto(p.url+class_url+'/external_tools/2')
        p.wait_for_load_state('networkidle')
        frame = p.frame_locator('.tool_launch').get_by_text('모든 주차')
        frame.click()

    def show_class(self):
        for i in self.classlist:
            print(self.classlist[i].title)
            print(self.classlist[i].url)

if __name__ == '__main__':
    with Pool(processes=mp.cpu_count()) as p:
        a = LearningX()
        b = LearningX()
        a.run()
        ret1 = p.apply_async(b.stream)   
        # p = Process(target=a.run)
        # b = Process(target=a.stream)
        p.close()
        p.join()


    
