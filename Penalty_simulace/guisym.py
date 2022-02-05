import tkinter as tk
import subprocess as sp
import win32gui    



class Simulace:
    def __init__(self,master):
        self.pc=[]
        frame=tk.Frame(master)
        
        tk.Label(frame,text="q:").grid(row=0,column=0)
        self.sl=tk.Scale(frame,from_=0,to=0.99,orient=tk.HORIZONTAL,resolution=0.001,length=200,
        activebackground="blue",tickinterval=0.99,takefocus=1)
        self.sl.grid(row=0,column=1)
        self.sl.set(0.5)
        tk.Label(frame,text="handicap:").grid(row=1,column=0)   
        self.sl2=tk.Scale(frame,from_=1.0,to=0.01,orient=tk.HORIZONTAL,resolution=0.001,length=200,
        activebackground="blue",tickinterval=1.0-0.01,takefocus=1)
        self.sl2.grid(row=1,column=1)
        self.sl2.set(1.0)
        tk.Label(frame,text="sc:").grid(row=2,column=0)
        self.sl3=tk.Scale(frame,from_=1,to=30,orient=tk.HORIZONTAL,resolution=1,
        activebackground="blue",tickinterval=30-1,takefocus=1)
        self.sl3.grid(row=2,column=1)
        self.sl3.set(15)
        
        
        but=tk.Button(frame,text="OK",command=self.launch).grid(row=3,column=1)
        master.bind("<Return>",self.on_enter)
        master.bind("k",lambda e: self.killall())
        master.bind("K",lambda e: self.killall())
        master.bind("q",lambda e: master.quit())
        master.bind("Q",lambda e: master.quit())
        frame.pack()    
        kbut=tk.Button(frame,text="killall",bg="red",command=self.killall)
        kbut.grid(row=3,column=2)
        
        frame.focus_set()
        #self.sl.focus()
        #win32gui.SetForegroundWindow(master.winfo_id())
        tk.mainloop()
    def launch(self):
        
        argstr=str(self.sl.get())+" "+str(self.sl2.get())+" "+str(self.sl3.get())
        print(argstr)
        self.pc.append(sp.Popen(("python simulacepen.py "
        +argstr).split()))
        
    def killall(self):
        for p in self.pc:
            p.terminate()
        self.pc=[]
    def on_enter(self,event):
        self.launch()

ap=tk.Tk()
Simulace(ap)
        
        