from playwright.sync_api import Page, expect ,sync_playwright
from heapq import heappush, nsmallest
import time
from multiprocessing import Queue 
from class_save import main_class ,todo_class

class SSU:
    def __init__(self):
        # heappush(SSU.class_list,C)
        self.main_class_list=[]
        self.class_list=[]
        self.curent_stream=1
        
    def add_todo_class(self,todo_class:todo_class):
        if not todo_class.isDone:
            heappush(self.class_list,todo_class)
    
    # @classmethod
    def add_main_class(self,c:main_class):
        self.main_class_list.append(c)

    def dump_frame_tree(self,frame, indent,stack=[]):
            # stack.append(indent + frame.name + '@' + frame.url)
            stack.append(frame.url)
            for child in frame.child_frames:
                self.dump_frame_tree(child, indent + "    ",stack)
            return stack
    
    # @classmethod
    def streaming(self,queue:Queue,page:Page):
        def send_message(message):
            print(f"put message in to :{message}")
            queue.put(message)
        
        def dump_frame_tree(frame, indent,stack=[]):
            stack.append(frame.url)
            for child in frame.child_frames:
                dump_frame_tree(child, indent + "    ",stack)
            return stack        
        try:
            current_ = nsmallest(self.curent_stream,self.class_list)[-1]
            self.now:todo_class = current_
        except IndexError:
            raise IndexError
        
        send_message("=====================================")
        send_message(self.now.class_status)
        send_message(f"TITLE:{self.now.title}")
        if (not self.now.isDone):
            page.goto(self.now.url)
            page.wait_for_load_state('networkidle')
            page.wait_for_load_state('domcontentloaded')
            frame= page.frame_locator('#tool_content').locator("#document")
            stack = dump_frame_tree(page.main_frame,"",[])
            check=False
            frame_url=''
            for i in stack:
                if "commons.ssu.ac.kr" in i:
                    frame_url=i
                    check=True
                    break;
            if check:
                page.goto(frame_url)
                page.wait_for_load_state('networkidle')
                #! debug
                # now.class_page.screenshot(path='1.png')
                start_btn = page.locator('.vc-front-screen-play-btn')
                start_btn.click()
                send_message("1.success")
                # now.class_page.screenshot(path='2.png')
                class_video = page.video
                # class_video.path()
                time.sleep(2)
                send_message("2.success")
                # now.class_page.screenshot(path='3.png')
                send_message("3.success")
                time.sleep(5)
                # now.class_page.screenshot(path='4.png')
                send_message("4.success")
                try:
                    loc = page.locator('#confirm-dialog')
                    loc.click()
                    continue_btn = page.locator(".confirm-ok-btn.confirm-btn")
                    expect(continue_btn)
                    continue_btn.click()
                    print("click continue")
                except:
                    send_message("is Not continue?")
                    pass
                time.sleep(1)
                page.screenshot(path='5.png')
                send_message("5.success")
                expect(page.locator(".vc-pctrl-play-progress"))
                class_video = page.video
                page.wait_for_load_state('domcontentloaded')
                page.locator("#play-controller")
                play_load = page.locator("#play-controller")
                get_progress= play_load.locator(".vc-pctrl-load-progress").get_attribute("style")
                # a = str(end_load.get_attribute("style"))
                current_progress = float(str(get_progress).split(":")[-1].split("%")[0].lstrip())
                if current_progress>=90:
                    time.sleep(2)
                    get_progress= play_load.locator(".vc-pctrl-load-progress").get_attribute("style")
                    # a = str(end_load.get_attribute("style"))
                    current_progress = float(str(get_progress).split(":")[-1].split("%")[0].lstrip())
                count = 0
                allow_upper_speed = page.locator(".confirm-ok-btn .confirm-btn")
                #=====================speed x2 =================================
                print(page.url)
                speed = page.locator('xpath=/html/body/div[1]/div[1]/div/div[9]/div/div/div[2]/div[13]/div[5]')
                speed.dispatch_event('click')
                print(speed.get_attribute('id'))
                # speed = play_load.query_selector("#vc-pctrl-playback-rate-20")
                # speed.click()
                # print(speed.get_attribute('class'))
                #================================================================
                # print(current_progress)
                while current_progress <= 90:
                    before_progress=current_progress
                    send_message(f"PROGRESS:{current_progress}")
                    send_message(f"current_speed : {speed.get_attribute('id')}")
                    time.sleep(1)
                    end_load= page.locator(".vc-pctrl-play-progress")
                    a = end_load.get_attribute('style')
                    current_progress = float(str(a).split(":")[-1].split("%")[0].lstrip())
                    if before_progress==current_progress:
                        page.locator(".confirm-ok-btn.confirm-btn").dispatch_event('click')
                        speed.dispatch_event('click')
                    # now.class_page.screenshot(path=f'{count}_.png')
                    count+=1
                self.now.check_done()
                send_message(f"end {self.now.title}")
            return 1
        else:
            self.curent_stream+=1
            try:
                k = self.streaming(queue,page)
            except RecursionError as e:
                print(e)
                return -1
            if k==-1:
                return
    def done_2_classlist(self,title):
        for cl in self.class_list:
            if cl.title==title:
                cl.isDone=True
                break

    def showing_main(self):
        for per_class in self.class_list:
            per_class:todo_class
            per_class.show()
    
    def showing_todo(self):
        for i in range(len(self.class_list)):
            cls2:todo_class = nsmallest(i+1,self.class_list)[-1]
            print("================================")
            print(cls2.title)
            print(cls2.url)
            print(cls2.rest_time)

    def get_todo(self):
        return self.class_list
    