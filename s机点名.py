import tkinter as tk
import random
def My_func():
    var.set("现在有请第%d组进行项目展示" % random.randint(1,3))
window = tk.Tk()
window.title('随机项目选择器 TSD1902版')
window.geometry('300x200')
var = tk.StringVar()
l =tk.Label(textvar=var,bg='sky blue',width=40,height=4)
l.pack()
but = tk.Button(text='下一组你所选择的项目是~',width=20,
    height=2,command=My_func)
but.pack()
window.mainloop()
