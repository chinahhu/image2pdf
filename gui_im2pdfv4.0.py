# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 19:17:36 2019

@author: Administrator
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import * 
import tkinter as tk  # 使用Tkinter前需要先导入
from tkinter import filedialog 
import threading
import os,re
import datetime,time
from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from PIL import Image 

def main():
    # 第1步，实例化object，建立窗口window
    window = tk.Tk()
    
    # 第2步，给窗口的可视化起名字
    window.title('Image2pdf')
     
    # 第3步，设定窗口的大小(长 * 宽)
    #window.geometry('650x550')  # 这里的乘是小x
    #window.resizable(width=False, height=False)
    
    # 第4步，在图形界面上创建一个标签label用以显示并放置
    #    第一个Label没有数据，，用于制造组键和边界的上间距。
    Label(window, text="").grid(row=0, pady=5,columnspan = 3)
    Label(window, text="").grid(row=5, pady=5,columnspan = 3)
    Label(window, text="").grid(column=0, padx=5)
    Label(window, text="").grid(column=7, padx=5)
    
    var00 = tk.StringVar()  # 创建变量
    lab00 = tk.Label(window,  textvariable=var00, bg='green', fg='white',font=('Arial', 12))
    lab00.grid(row=6,column=1 )
    
    # 设置下载进度条
    progbar = tk.Canvas(window, width=200, height=22, bg="white")
#    progbar = tk.progbar(window, bg="white")
    progbar.grid(row=6,column=2,sticky=W )
   
    
    # 显示---输入输出目录
    var1 = tk.StringVar()  # 创建变量
    lab1 = tk.Entry(window,  textvariable=var1)
    lab1.grid(row=1,column=2,pady=5)
    
    var3 = tk.StringVar()  # 创建变量
    lab3 = tk.Entry(window, textvariable=var3)
    lab3.grid(row=2,column=2,pady=5)
    
    # 创建sby
    sbx = Scrollbar(window,orient=HORIZONTAL)    #水平滚动条组件
    sbx.grid(row=5,column=2,sticky=N+EW)
    sby = Scrollbar(window, orient=VERTICAL)    #垂直滚动条组件
    sby.grid(row=4,column=3,sticky=W+NS)  #right side
    
    
     #图片类型格式
    v=IntVar()
    im_types=[('.gif',0),('.jpg',1),('.jpeg',2),('.png',3)]
    
    def callRB():
        global imtype
        for i in range(4):
            if v.get()==i:
#                print('你的选择是'+im_types[i][0]+'!') 
                imtype=im_types[i][0]
     
    # 创建 radio
#    imrad0=tk.Radiobutton(window, text=im_types[0][0], command=callRB, variable=v)
#    imrad1=tk.Radiobutton(window, text=im_types[1][0], command=callRB, variable=v)
#    imrad2=tk.Radiobutton(window, text=im_types[2][0], command=callRB, variable=v)
#    imrad3=tk.Radiobutton(window, text=im_types[3][0], command=callRB, variable=v)
#    imrad0.grid(row=3,column=1,sticky=W+NS)
#    imrad1.grid(row=3,column=2,sticky=W+NS)
#    imrad2.grid(row=4,column=1,sticky=W+NS)
#    imrad3.grid(row=5,column=1,sticky=W+NS)
    for lan,num in im_types:
        imrad0=tk.Radiobutton(window, text=lan, value=num, command=callRB, variable=v)
        imrad0.grid(row=3+num,column=0,sticky=W+NS)
    
    # 创建Listbox 
    var2 = tk.StringVar()
    lb = tk.Listbox(window,listvariable=var2)  #,yscrollcommand=sby.set
    lb.grid(row=4,column=2,pady=5) 
    
    lb['yscrollcommand'] = sby.set
    lb['xscrollcommand'] = sbx.set
    sbx['command'] = lb.xview
    sby['command'] = lb.yview
    
   
   
         
    # 第6步，创建一个方法用于按钮的点击事件
    
    def open_dir():
        global impath, input_paths
        folder =filedialog.askdirectory()
    #    tkFileDialog.askdirectory
        files0 = os.listdir(folder)
        
        # 筛选图片格式格式
        pics0 = [files0
                      for files0 in os.listdir(folder)                         
                      if files0.endswith(imtype)]#, '.png', '.jpeg'))]
#                      if files0.endswith(('.gif'))]#, '.png', '.jpeg'))]
    #    print(pics0)
        # 按照文件排序
        pics11=sort_files(pics0)
    #    print(pics11)
        input_paths = [folder  +"/"+ kk+imtype
#        input_paths = [folder  +"/"+ kk+".gif"
                      for kk  in pics11 ]                       
    #                  if files0.endswith(('.gif', '.png', '.jpeg'))]
    #                  if music.endswith(('.mp3', '.wav', '.ogg'))]
       
        var1.set(folder)  # 为label设置值
    #    if len(files0):
        if input_paths:
            var2.set(input_paths)
#            sby.config(command=lb.yview)
    #        print('Yes')
        else:
            var2.set(['No Image Files!'])
    #        print('No')
            
        impath = input_paths[1]
    
    def set_dir():
        global output1
    #    filename=input('please input your pdf name: ')
        pdffile= "test_%s.pdf" %datetime.datetime.now().strftime('%M%S')
        folder1 = filedialog.askdirectory()
        output1=folder1+'/'+pdffile
        var3.set(output1)  # 为label设置值
        
    def sort_files(list0):
        ls0=[] 
        for kk in list0:
                ls0.append(kk.split(imtype)[0])
#                ls0.append(kk.split('.gif')[0])
        ls0.sort(key=lambda d:int(d))
        return ls0
    
    def thread_method():
      t1 = threading.Thread(target=start_pdf)
      t1.start()
#      t2 = threading.Thread(target=progress)
#      t2.start()
      
    def start_pdf():
        output0=var3.get()
        
#        fill_line = progbar.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
        x=len(input_paths)
        
        (maxw, maxh) = Image.open(impath).size
        if output0==output1:
            c = canvas.Canvas(output0, pagesize=portrait((maxw, maxh)))
        else:
            c = canvas.Canvas(output0, pagesize=portrait((maxw, maxh)))
            
        for kk in range(len(input_paths)):
                c.drawImage(input_paths[kk], 0, 0, maxw, maxh)
                c.showPage()      
#                str0=['正在转换第 %d'% (kk+1),'共 %d'%len(input_paths)]
                str1='正在转换第 %d'% (kk+1)
#                str1=['正在转换第 %d'% (kk+1),'共 %d'%p0]
                var00.set(str1)
                change_schedule(2*kk,x) 
                
        c.save() 
        var00.set('转换完毕！')
        tk.messagebox.showinfo(title='Hi', message='转换成功！')       
  
    def change_schedule(now_schedule,all_schedule):
        fill_rec = progbar.create_rectangle(5,5,5,25,outline = "",width = 0,fill = "green")
        progbar.coords(fill_rec, (5, 5, 6 + (now_schedule/all_schedule)*100, 25))
        window.update()
      
    # 第5步，创建一个按钮并放置，点击按钮调用print_selection函数
    b1 = tk.Button(window, text='open dir...', command=open_dir)
    b1.grid(row=1,column=1,pady=5)
    
    b2 = tk.Button(window, text='output dir...', command=set_dir)
    b2.grid(row=2,column=1,sticky=E,pady=5)
    
    b3 = tk.Button(window, text='Start...', command=thread_method)
    b3.grid(row=3,column=2,pady=5)
  
# 第8步，主窗口循环显示
    window.mainloop()

if __name__ == "__main__":
    main()
