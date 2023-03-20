import tkinter
import tkinter.messagebox
import customtkinter 
import time
import learn_x2
import threading
import webbrowser
from heapq import nsmallest
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
from class_save import todo_class,main_class
from multiprocessing import Queue

class App(customtkinter.CTk):
    def __init__(self,queue:Queue,classlist,todo_classlist,learningX:learn_x2.LearningX):
        super().__init__()
        self.queue=queue
        self.classlist= classlist
        self.todo_classlist = todo_classlist
        self.learning= learningX #Learning X
        # print(self.lea)
        self.carry = self.learning.get_classlist()
        
        self.title("SSU AUTO MATION BY .KIRU")
        
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
        for i,class_name in enumerate(self.classlist):
            button = customtkinter.CTkButton(master=self.sidebar_frame_class, text=f"{class_name}",command=self.sidebar_button_event)
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
        
        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Log")
        self.entry.grid(row=2, rowspan=2,column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        # self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250,height=1)
        self.textbox.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # self.textbox.configure(state="disabled")
        #! EX)
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
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("Assigment").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Assigment"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("Assigment"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Assigment"), text="Open CTkInputDialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # create slider and progressbar frame
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
        
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # set default values
        # self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        # self.checkbox_3.configure(state="disabled")
        self.checkbox_1.select()
        # self.scrollable_frame_switches[0].select()
        # self.scrollable_frame_switches[4].select()
        self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("CTkOptionmenu")
        self.combobox_1.set("CTkComboBox")
        
        # self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua")
        

        # self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        # self.seg_button_1.set("Value 2")
    def switch_toggle(self,switch:customtkinter.CTkSwitch):
        if switch.get()==0:
            self.learning.ssu.done_2_classlist(switch.text)
            print(switch.text)            
        
            
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    
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

    def sidebar_button_event(self):
        pass
        
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
    
