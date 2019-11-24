# noinspection PyCompatibility
import tkinter as tk

from project.app import App

if __name__ == "__main__":
    """
    facade
    author: huobaolajiao, adminerest
    """
    root = tk.Tk()
    app = App(root)
    root.title('urp评教小助手')
    root.mainloop()
