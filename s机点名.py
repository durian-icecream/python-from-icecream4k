import tkinter as tk
import random
list_test = ["谷学曾","万逸南","余志童","吴子祥","谢倩文",
              "郭丹红","李晶","张颖颖","吕屹","柴焕","段胜利"]
def My_func():
    var.set(list_test[random.randint(1,len(list_test)-1)])
window = tk.Tk()
window.title('随机点名选择器 TSD2005版')
window.geometry('300x200')
var = tk.StringVar()
l =tk.Label(textvar=var,bg='sky blue',width=40,height=4)
l.pack()
but = tk.Button(text='下一个你所选择的人是~',width=20,
    height=2,command=My_func)
but.pack()
window.mainloop()
