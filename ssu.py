from playwright.sync_api import Page, expect ,sync_playwright
from heapq import heappop,heapify,heappush, nsmallest
import time
class main_class:
    def __init__(self,title,url,class_page:Page) -> None:
        self.title= title
        self.url = url
        self.pdf_url = []
        self.file_url=[]
        self.assginment=[]
        self.class_title_list=dict()
        self.class_list_error=set()
        self.class_page= class_page
        

# https://canvas.ssu.ac.kr
# /learningx/
# coursebuilder
# /course/16657/
# learn/274876
# /unit/2165296/
# view?user_id=11806
# &user_login=20180354
# &user_name=%EA%B9%80%EA%B8%B0%ED%9B%88(20%23%23%23%2354)
# &user_email=rlarlgnszx%40naver.com
# &role=1&is_observer=false&locale=ko&mode=default

 
class todo_class:
    def __init__(self,title,url,rest_time,class_status,class_page:Page):
        self.title= title
        self.url = url
        self.rest_time=rest_time
        self.isDone = False
        self.class_status = class_status
        # print(type(self.class_status))
        temping = self.rest_time.rstrip()
        if "시간" in temping:
            temping = temping.split("시간")
            self.rest_time = int(temping[0])-24
        else:
            temping =self.rest_time.split("-")
            if len(temping)>=2:
                self.rest_time=int(temping[1])
            else:
                self.rest_time=float('inf')
                self.isDone=True
        self.class_page= class_page

    def __lt__(self,other):
        return other.rest_time > self.rest_time


    
class SSU:
    main_class_list= []
    class_list=[]
    current_stream=0
    def __init__(self,C:todo_class):
        heappush(SSU.class_list,C)
    
    @classmethod
    def add_main_class(cls,c:main_class):
        SSU.main_class_list.append(c)

    def dump_frame_tree(self,frame, indent,stack=[]):
            # stack.append(indent + frame.name + '@' + frame.url)
            stack.append(frame.url)
            for child in frame.child_frames:
                self.dump_frame_tree(child, indent + "    ",stack)
            return stack
    
    @classmethod
    def showing_main(cls):
        pass
    
    @classmethod
    def streaming(cls):
        def dump_frame_tree(frame, indent,stack=[]):
            # stack.append(indent + frame.name + '@' + frame.url)
            stack.append(frame.url)
            for child in frame.child_frames:
                dump_frame_tree(child, indent + "    ",stack)
            return stack
        now:todo_class = SSU.class_list[SSU.current_stream]
        print("=====================================")
        print(now.class_status)
        print(now.title)
        if (not now.isDone) and "video" in now.class_status:
            now.class_page.goto(now.url)
            now.class_page.wait_for_load_state('networkidle')
            now.class_page.wait_for_load_state('domcontentloaded')
            frame= now.class_page.frame_locator('#tool_content').locator("#document")
            stack = dump_frame_tree(now.class_page.main_frame,"",[])
            check=False
            frame_url=''
            for i in stack:
                if "commons.ssu.ac.kr" in i:
                    frame_url=i
                    check=True
                    break;
            if check:
                now.class_page.goto(frame_url)
                now.class_page.wait_for_load_state('networkidle')
                now.class_page.screenshot(path='1.png')
                start_btn = now.class_page.locator('.vc-front-screen-play-btn')
                start_btn.click()
                print("1.save")
                now.class_page.screenshot(path='2.png')
                class_video = now.class_page.video
                # class_video.path()
                time.sleep(2)
                print("2.save")
                now.class_page.screenshot(path='3.png')
                print("3.save")
                time.sleep(5)
                now.class_page.screenshot(path='4.png')
                print("4.save")
                try:
                    loc = now.class_page.locator('#confirm-dialog')
                    loc.click()
                    continue_btn = now.class_page.locator(".confirm-ok-btn.confirm-btn")
                    expect(continue_btn)
                    continue_btn.click()
                    print("click continue")
                except:
                    print("is Not continue?")
                    pass
                time.sleep(1)
                now.class_page.screenshot(path='5.png')
                print("5.save")
                expect(now.class_page.locator(".vc-pctrl-play-progress"))
                class_video = now.class_page.video
                now.class_page.wait_for_load_state('domcontentloaded')
                now.class_page.locator("#play-controller")
                play_load = now.class_page.locator("#play-controller")
                
                get_progress= play_load.locator(".vc-pctrl-load-progress").get_attribute("style")
                # a = str(end_load.get_attribute("style"))
                current_progress = float(str(get_progress).split(":")[-1].split("%")[0].lstrip())
                if current_progress>=90:
                    time.sleep(2)
                    get_progress= play_load.locator(".vc-pctrl-load-progress").get_attribute("style")
                    # a = str(end_load.get_attribute("style"))
                    current_progress = float(str(get_progress).split(":")[-1].split("%")[0].lstrip())
                count = 0
                allow_upper_speed = now.class_page.locator(".confirm-ok-btn .confirm-btn")
                #=====================speed x2 =================================
                print(now.class_page.url)
                speed = now.class_page.locator('xpath=/html/body/div[1]/div[1]/div/div[9]/div/div/div[2]/div[13]/div[5]')
                speed.dispatch_event('click')
                print(speed.get_attribute('id'))
                # speed = play_load.query_selector("#vc-pctrl-playback-rate-20")
                # speed.click()
                # print(speed.get_attribute('class'))
                #================================================================
                print(current_progress)
                while current_progress <= 90:
                    before_progress=current_progress
                    print(f"current progress : {current_progress}")
                    print("current_speed : ",speed.get_attribute('id'))
                    time.sleep(1)
                    end_load= now.class_page.locator(".vc-pctrl-play-progress")
                    a = end_load.get_attribute('style')
                    current_progress = float(str(a).split(":")[-1].split("%")[0].lstrip())
                    if before_progress==current_progress:
                        now.class_page.locator(".confirm-ok-btn.confirm-btn").dispatch_event('click')
                        speed.dispatch_event('click')
                    # now.class_page.screenshot(path=f'{count}_.png')
                    count+=1
                now.isDone=True
                print(f"end {now.title}")
            return 1
        else:
            SSU.current_stream+=1
            SSU.streaming()
    
    @classmethod
    def showing_todo(cls):
        for i in range(len(SSU.class_list)):
            cls2 = nsmallest(i+1,SSU.class_list)[-1]
            print("================================")
            print(cls2.title)
            print(cls2.url)
            print(cls2.rest_time)

    