import tkinter
import tkinter.messagebox

top = tkinter.Tk()
top.minsize(300,200)
def helloCallBack():
   tkinter.messagebox.showinfo( "Hello Python", "Hello Runoob")
 
B = tkinter.Button(top, text ="点我", command = helloCallBack)
 
B.pack()
top.mainloop()