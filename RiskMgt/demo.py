import tkinter
import tkinter.messagebox
def but():
    a=tkinter.messagebox.askokcancel('提示', '要执行此操作吗')
    print (a)
root=tkinter.Tk()
root.title('GUI')#标题
root.geometry('800x600')#窗体大小
root.resizable(False, False)#固定窗体
tkinter.Button(root, text='hello button',command=but).pack()
root.mainloop()
'''
from tkinter import *
from pandastable import Table, TableModel

class TestApp(Frame):
    """Basic test frame for the table"""
    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('600x400+200+100')
        self.main.title('Table app')
        f = Frame(self.main)
        f.pack(fill=BOTH,expand=1)
        df = TableModel.getSampleData()
        self.table = pt = Table(f, dataframe=df,
                                showtoolbar=True, showstatusbar=True)
        pt.show()
        return

app = TestApp()
#launch the app
app.mainloop()





import tkinter  
from tkinter import ttk  # 导入内部包  


li = ['王记','12','男']  
root = tkinter.Tk()  
root.title('测试')  

tree = ttk.Treeview(root,columns=['1','2','3'],show='headings',selectmode='browse')  
tree.column('1',width=100,anchor='center')  
tree.column('2',width=100,anchor='center')  
tree.column('3',width=100,anchor='center')  
tree.heading('1',text='姓名')  
tree.heading('2',text='学号')  
tree.heading('3',text='性别')  
tree.insert('','end',text='1',values=li)  
tree.insert('','end',text='2',values=li)
tree.focus()
tree.grid()  

  
def treeviewClick(event):#单击  
    print ('单击')  
    for item in tree.selection():  
        item_text = tree.item(item,"values")  
        print(item_text[0])#输出所选行的第一列的值  
  
tree.bind('<ButtonRelease-1>', treeviewClick)#绑定单击离开事件===========  
  
root.mainloop()  


from tkinter import *
from pandastable import Table, TableModel
root = Tk() 
f = Frame(root)
f.pack(fill='both',expand=1)
df = TableModel.getSampleData()
table = pt = Table(f, dataframe=df)
table.show()
root.mainloop()




class TestApp(Frame):
    """Basic test frame for the table"""
    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('600x400+200+100')
        self.main.title('Table app')
        f = Frame(self.main)
        f.pack(fill=BOTH,expand=1)
        df = TableModel.getSampleData()
        self.table = pt = Table(f, dataframe=df,
                                showtoolbar=True, showstatusbar=True)
        pt.show()
        return

app = TestApp()
#launch the app
app.mainloop()
'''