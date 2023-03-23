import tkinter.messagebox
import customtkinter 
import tkinter
import time
import learn_x2
import threading
from PIL import Image
from heapq import nsmallest
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
from class_save import todo_class,main_class
from multiprocessing import Queue
import os
class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(anchor='NSEW',padx=20, pady=20)

class App(customtkinter.CTk):
    def __init__(self,queue:Queue,classlist,todo_classlist,learningX:learn_x2.LearningX):
        super().__init__()
        self.queue=queue
        self.classlist= classlist
        self.todo_classlist = todo_classlist
        self.learning= learningX #Learning 
        self.carry = self.learning.get_classlist()
        self.main_classlist=None
        self.title("SSU AUTO MATION BY .KIRU")
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.geometry(f"{1300}x{700}")
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((2, 1, 1), weight=1)
        self.index=0
        
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0,rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(3, weight=1)
        self.sidebar_frame_class = customtkinter.CTkScrollableFrame(self.sidebar_frame, corner_radius=0,label_text="강의")
        self.sidebar_frame_class.grid(ipady=80, ipadx=30,column=0, padx=15 ,pady=(20,0), sticky="nsew")
        
        self.scrollable_frame_button = []
        self.button_box = [0 for x in range(len(self.classlist))]
        for i,class_name in enumerate(self.classlist):
            button=customtkinter.CTkButton(master=self.sidebar_frame_class, text=f"{class_name}",command=lambda c=i:self.sidebar_button_event(c))
            button.grid(row=i, column=0, padx=20, pady=(25,0))
            self.scrollable_frame_button.append(button)

        self.stream_button = customtkinter.CTkButton(master=self.sidebar_frame, text="STREAM",command=self.stream_button_event,fg_color="#58CCBB",hover_color="#0A7666",text_color='#1E352B')
        self.stream_button.grid(row=2, column=0, padx=20, pady=(25,0))
        
        self.download_button = customtkinter.CTkButton(master=self.sidebar_frame, text="DOWNLOAD",command=self.download_button_event,fg_color="#58CCBB",hover_color="#0A7666",text_color='#1E352B')
        self.download_button.grid(row=3, column=0, padx=20, pady=(25,0))
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=4, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create textbox
        # create main entry and button
        self.textbox = customtkinter.CTkTextbox(self, width=250,height=1)
        self.textbox.grid(row=2, rowspan=2,column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # self.textbox.configure(state="disabled")

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="할일 목록")
        self.scrollable_frame.grid(row=0, column=1, padx=(10, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        
        self.todo_classlist.sort()
        for i in range(len(self.todo_classlist)):
            # cls2 = nsmallest(i+1,self.todo_classlist)[-1]
            cls2= self.todo_classlist[i]
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"{cls2.title}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)
        
        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Assigment")
        self.tabview.add("notice")
        self.tabview.tab("Assigment").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("notice").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Assigment"),
                                                        values=['',''], command=self.show_image2)
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("notice"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)
        
        self.toplevel_window = None
        
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.slider_class = customtkinter.CTkLabel(self.slider_progressbar_frame,text="소 클래스 이름",font=customtkinter.CTkFont("Arial", 18))
        self.slider_class.grid(row=0, column=0, padx=40, pady=(10, 10), sticky="ew")
        self.slider_class2 = customtkinter.CTkLabel(self.slider_progressbar_frame,text="진행도")
        self.slider_class2.grid(row=1, column=0, padx=40, pady=(10, 10), sticky="ew")
       
        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame,progress_color="#58CCBB")
        self.progressbar_2.grid(row=4, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        
        self.progress_per = customtkinter.CTkLabel(self.slider_progressbar_frame,text=f"{self.progressbar_2.get()}%")
        self.progress_per.grid(row=5, column=0, padx=40, pady=(10, 10), sticky="ew")
        
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("CTkOptionmenu")
        
        self.image= customtkinter.CTkImage(Image.open(os.path.join(self.image_path,"bg_gradient.jpg")),size=(30,30),master=self.tabview.tab['Assignment'])
        print("image load ok")

        self.image_frame = customtkinter.CTkLabel(master=self.tabview.tab("Assigment"),image=self.image)
        self.image_frame.grid(column=2,row=1,rowspan=2,columnspan=2,sticy='nsew')
        
    def switch_toggle(self,switch:customtkinter.CTkSwitch):
        if switch.get()==0:
            self.learning.ssu.done_2_classlist(switch.text)
            print(switch.text)            
    def class_button_click(self):
        pass
            
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkToplevel(text="Type in a number:", title="CTkInputDialog")
        # print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()  # if window exists focus it
    
    def receive_msg(self):
        print("=======recevie server start=======")
        if self.queue.empty():
            message = "AUTO STARTING..."
        while 1:
            time.sleep(0.15)
            if self.queue.qsize() > 0: 
                # print("qeueu alive")              
                message = self.queue.get()
                if message=='end get class':
                    print("===============received server end=============")
                    break
                elif message.startswith('PROGRESS'):
                    self.progress_up(float(float(message.split(":")[1])/100))
                    # self.text_delete()
                elif message.startswith('TITLE'):
                    title=message.split(":")[1]
                    self.slider_class.configure(text=title)
                else:
                    self.text_log_input(message)
        return

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def stream_button_event(self):
        self.text_log_input("\n\n=====Learning X Auto Stream Start=====\n" )
        p1 = threading.Thread(target=self.learning.stream)
        p1.start()
        receive_check =threading.Thread(target=self.receive_msg)
        receive_check.start()
    
    def download_button_event(self):
        self.text_log_input("\n\n=====Learning X Auto Download Start=====\n" )
        p2 = threading.Thread(target=self.learning.run,args=(True,))
        p2.start()
        receive_check =threading.Thread(target=self.receive_msg)
        receive_check.start()

    def show_image2(self,choice):
        path='123'
        todo_class_per:todo_class
        print("assignment:",len(self.assigment.get_assignment()))
        for todo_class_per in self.assigment.get_assignment():
            print(todo_class_per.title)
            print(todo_class_per.get_image_path())
            if choice in todo_class_per.title:
                path = todo_class_per.get_image_path()
                break
            
        # self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/test_images/bg_gradient.jpg"),
        #                                        size=(self.width, self.height))
        # self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        # self.bg_image_label.grid(row=0, column=0)
        self.image =customtkinter.CTkImage(Image.open(path),size=(30,30))
        self.image_frame.configure(image=self.image)
        
    def sidebar_button_event(self,i):
        text = self.scrollable_frame_button[i].cget("text")
        self.click_button = text
        self.main_classlist=self.learning.get_classlist()
        for cls in self.main_classlist:
            if text in cls:
                self.assigment:main_class=self.main_classlist[cls]
                break
        self.optionmenu_1.configure(values=[x.title for x in self.assigment.get_assignment()])
        
    def progress_up(self,current_progress):
        self.progressbar_2.set(current_progress)
        self.progressbar_2._draw()
        current_progress = "{:.2f}".format(current_progress*100)
        self.progress_per.configure(text=f"{current_progress}%")
    
    
    def text_log_input(self,msg):
        self.textbox.insert("0.0",f"\n{msg}")
    
    def text_delete(self):
        self.textbox.delete("0")
    
    def progress_start(self):
        for i in range(100):
            time.sleep(0.1)
    
if __name__ == "__main__":
    print("not start it first")
    
