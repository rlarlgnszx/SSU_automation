import customtkinter
from PIL import Image 
import os
import learn_x2
import ssu_ui
customtkinter.set_appearance_mode("dark")
from multiprocessing import Queue
import os
import time
from dotenv import load_dotenv,find_dotenv ,set_key

class LoginErrorWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.label = customtkinter.CTkLabel(self, text="ID랑 비밀번호를 다시 입력해주세요")
        self.label.pack(padx=20, pady=20)

class App(customtkinter.CTk):
    width = 900
    height = 600
    def __init__(self, *args, **kwargs,):
        super().__init__(*args, **kwargs)    
        self.queue=Queue()
        self.title("SSU AutoMation feat. Kiru")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        load_dotenv()
        self.dotenv_file = find_dotenv()
        load_dotenv(self.dotenv_file)
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/test_images/bg_gradient.jpg"),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)
        self.toplevel_window = None
        self.after_login_window=None
        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="SSU AutoMation \nfeat. Kiru",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_event, width=200)
        self.login_button.grid(row=3, column=0, padx=30, pady=(15, 15))
        # create main frame
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_label = customtkinter.CTkLabel(self.main_frame, text=f"Hello \n{self.username_entry.get()}",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.main_label.grid(row=0, column=0, padx=30, pady=(30, 15))
        self.checkbox = customtkinter.CTkCheckBox(self.login_frame,text="REMEMBER?",onvalue="on",offvalue="off",command=self.checkbox_event)
        self.checkbox.grid(row=4, column=0, pady=(20, 0), padx=20, sticky="n")
        try:
            if os.environ['CHECK']=="1":
                self.checkbox.select()
        except:
            pass
    
    def checkbox_event(self):
        print(self.checkbox.get())
    #! Login EVENT
    def login_ok(self):
        if self.checkbox.get()=="on":
            set_key(self.dotenv_file,"CHECK","1")
            if self.username_entry.get() !="":
                os.environ['ID'] = self.username_entry.get() 
                set_key(self.dotenv_file,"ID",self.username_entry.get())
            if self.password_entry.get() !="":
                os.environ["PW"] = self.password_entry.get()
                set_key(self.dotenv_file,"PW",self.password_entry.get())
            load_dotenv(self.dotenv_file)
            set_key(self.dotenv_file,"CHECK","1")
    
    def login_event(self):
        a = time.time()
        print("Login pressed - username:", self.username_entry.get(), "password:", self.password_entry.get())
        self.running = learn_x2.LearningX(self.queue)
        is_login = self.running.checking_ID_PW(self.username_entry.get(),self.password_entry.get())
        if is_login:
            self.login_ok()
            self.login_frame.grid_forget()
            self.classlist = self.running.run(False)
            self.todo_classlist = self.running.get_todo_2_dict()
            self.classlist = self.class_mining(self.classlist)
            if self.after_login_window is None or not self.after_login_window.winfo_exists():
                self.after_login_window = ssu_ui.App(self,queue=self.queue,classlist=self.classlist,todo_classlist=self.todo_classlist,learningX=self.running)
            else:
                self.after_login_window.focus()
            # self.next = ssu_ui.App(self.queue,self.classlist,self.todo_classlist,self.running)
            b = time.time()
            print(b-a,"time")
        else:
            if self.queue.get():
                print("WOW ERR!")
        return True
    
    def open_login_error(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = LoginErrorWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()
    
    def class_mining(self,data):
        classes = {}
        for da in data:
            fi = da.split(")")[0]
            fi+=")"
            classes[fi]=data[da]
        return classes
    
    def run(self):
        self.mainloop()
    
if __name__ == "__main__":
    app = App()
    app.run()