from tkinter import *
from extendspace import extend as ex

class Extend():
    def __init__(self):
        self.root = Tk()
        self.root.geometry('460x460')
        self.root.title('extendspace')

        self.lb1 = Label(self.root, text='请输入下列信息进行表空间扩容')
        self.lb1.place(relx=0.3, rely=0.03, relwidth=0.4, relheight=0.05)
        self.lb3 = Label(self.root, text='IP地址')
        self.lb3.place(relx=0.07, rely=0.1, relwidth=0.1, relheight=0.05)
        self.lb4 = Label(self.root, text='用户名')
        self.lb4.place(relx=0.07, rely=0.2, relwidth=0.1, relheight=0.05)
        self.lb5 = Label(self.root, text='密码')
        self.lb5.place(relx=0.07, rely=0.3, relwidth=0.1, relheight=0.05)
        self.lb6 = Label(self.root, text='数据库')
        self.lb6.place(relx=0.07, rely=0.4, relwidth=0.1, relheight=0.05)

        self.inp1 = Entry(self.root)
        self.inp1.place(relx=0.2, rely=0.1, relwidth=0.7, relheight=0.05)
        self.inp2 = Entry(self.root)
        self.inp2.place(relx=0.2, rely=0.2, relwidth=0.7, relheight=0.05)
        self.inp3 = Entry(self.root)
        self.inp3.place(relx=0.2, rely=0.3, relwidth=0.7, relheight=0.05)
        self.inp4 = Entry(self.root)
        self.inp4.place(relx=0.2, rely=0.4, relwidth=0.7, relheight=0.05)

        # 方法一导出直接调用 run1()
        self.btn1 = Button(self.root, text='确定', command=self.run1)
        self.btn1.place(relx=0.4, rely=0.5, relwidth=0.2, relheight=0.05)

        # 在窗体垂直自上而下位置60%处起，布局相对窗体高度40%高的文本框
        self.txt = Text(self.root)
        self.txt.place(rely=0.6, relwidth=1, relheight=0.4)

        self.root.mainloop()

    def run1(self):
        host = str(self.inp1.get())
        user = str(self.inp2.get())
        pwd = str(self.inp3.get())
        dbname = str(self.inp4.get())
        ep = ex.Alterspace(host, user, pwd, dbname)
        s = ep.createdatafile()
        self.txt.insert(END, s)  # 追加显示运算结果
        # inp1.delete(0, END)  # 清空输入
        # inp2.delete(0, END)  # 清空输入
        # inp3.delete(0, END)  # 清空输入
        # inp4.delete(0, END)  # 清空输入


a=Extend()