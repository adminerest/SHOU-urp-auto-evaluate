import threading
from evaluation import Evaluation
import tkinter as tk

# @author: huobaolajiao


class App:
    def __init__(self, root):
        self.labelusr = tk.Label(root, text='学号：')
        self.labelusr.grid(row=0, sticky=tk.W)
        self.username = tk.StringVar()
        tk.Entry(root, textvariable=self.username). grid(row=0, column=1)
        self.labelpw = tk.Label(root, text='密码：')
        self.labelpw.grid(row=1, sticky=tk.W)
        self.password = tk.StringVar()
        tk.Entry(root, textvariable=self.password, show='*').grid(row=1, column=1)
        self.labelcode = tk.Label(root, text='验证码：')
        self.labelcode.grid(row=2, sticky=tk.W)
        self.code = tk.StringVar()
        tk.Entry(root, textvariable=self.code).grid(row=2, column=1)
        self.button1 = tk.Button(root, text="登陆", command=self.prelogin)
        self.button1.grid(row=3, column=0)
        self.button2 = tk.Button(root, text="更换验证码", command=self.prechange)
        self.button2.grid(row=3, column=2)
        self.info = tk.LabelFrame(root, text='信息栏：                   ')
        self.error = tk.StringVar()
        self.info.grid(row=4, column=1)
        self.Labelerr = tk.Label(self.info, textvariable=self.error, wraplength=130, height=2)  # 可调整调试内容文本框高度
        self.Labelerr.grid()
        self.eva = Evaluation(self.error)
        self.labelimg = tk.Label(root)
        self.labelimg.grid(row=2, column=2)
        self.prechange()

    def prelogin(self):
        self.thread = threading.Thread(target=self.login)
        self.thread.setDaemon(True)
        self.thread.start()  # 调用evaluation是超长时间任务,界面会假死，所以开个新进程

    def login(self):
        self.button1.configure(state='disabled')
        self.button2.configure(state='disabled')
        user = self.username.get()
        password = self.password.get()
        code = self.code.get()
        if self.eva.login(user, password, code):  # 传入文本框中三个参数
            self.eva.evaluate()
        self.change()
        self.button1.configure(state='normal')
        self.button2.configure(state='normal')

    def prechange(self):
        self.thread = threading.Thread(target=self.change)
        self.thread.setDaemon(True)
        self.thread.start()

    def change(self):
        self.button1.configure(state='disabled')
        self.button2.configure(state='disabled')
        tk_image = self.eva.get_login_img()
        self.labelimg.configure(image=tk_image)
        self.labelimg.image = tk_image
        self.button1.configure(state='normal')
        self.button2.configure(state='normal')
