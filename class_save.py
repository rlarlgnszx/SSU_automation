from playwright.sync_api import Page
from heapq import heappop,heappush
import datetime as dt
class main_class:
    def __init__(self,title,url,class_page:Page) -> None:
        self.title= title
        self.url = url
        self.pdf =[]
        self.file=[]
        self.video = []
        self.assginment=[]
        self.class_title_list=dict()
        self.class_list_error=set()
        self.class_page= class_page
    
    def add_property(self,title,url,status,rest_time):
        temp_todo = todo_class(title,url,status,self.title,self.class_page,rest_time)
        if "pdf" in status:
            heappush(self.pdf,temp_todo)
        elif "everlec" in status:
            heappush(self.video,temp_todo)
        elif "file" in status:
            heappush(self.file,temp_todo)
        elif "assignment" in status:
            heappush(self.assginment,temp_todo)
    def show(self):
        print("pdf:",self.pdf)
        print("video:",self.video)
        print("file",self.file)
        
    def get_file(self):
        return self.file
    
    def get_pdf(self):
        return self.pdf
    
    def get_video(self):
        return self.video
    
    def get_assignment(self):
        return self.assginment
    
class todo_class:
    def __init__(self,title,url,class_status,main_class_name,page:Page,rest_time=''):
        self.title= title
        self.url = url
        self.rest_time=rest_time
        self.isDone = False
        self.class_status = class_status
        self.main_class_name =main_class_name
        self.class_page= page
        self.is_fail=False
        if self.rest_time=='':
            self.rest_time = dt.datetime.strptime("12월 31일 오후 11:59", "%m월 %d일 오후 %H:%M")
            self.rest_time.replace(year=2024)
            self.isDone=True
        self.image_path:str =''
    
    def __lt__(self,other):
        return other.rest_time > self.rest_time
    
    def check_done(self):
        self.isDone=True
    def change_title(self,name):
        self.title = name
    def show(self):
        print(f"title : {self.title}")
        print(f"url : {self.url}")
        print(f"rest time : {self.rest_time}")
        print(f"is Done :{self.isDone}")
        print(f"class_status : {self.class_status}")

    def set_image_path(self,path):
        self.image_path = path
    def get_image_path(self):
        return self.image_path