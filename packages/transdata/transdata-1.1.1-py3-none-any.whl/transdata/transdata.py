from tkinter import *
from transdata import exportdata as ep
from transdata import importdata as id

class Transdata():
    def __init__(self):
        self.root = Tk()
        self.root.geometry('460x460')
        self.root.title('transdata')

        self.lb1 = Label(self.root, text='请输入下列信息进行导出')
        self.lb1.place(relx=0.1, rely=0.03, relwidth=0.3, relheight=0.05)
        self.lb2 = Label(self.root, text='请输入下列信息进行导入')
        self.lb2.place(relx=0.6, rely=0.03, relwidth=0.3, relheight=0.05)
        self.lb3 = Label(self.root, text='IP地址')
        self.lb3.place(relx=0.01, rely=0.1, relwidth=0.1, relheight=0.05)
        self.lb4 = Label(self.root, text='用户名')
        self.lb4.place(relx=0.01, rely=0.2, relwidth=0.1, relheight=0.05)
        self.lb5 = Label(self.root, text='密码')
        self.lb5.place(relx=0.01, rely=0.3, relwidth=0.1, relheight=0.05)
        self.lb6 = Label(self.root, text='数据库')
        self.lb6.place(relx=0.01, rely=0.4, relwidth=0.1, relheight=0.05)
        self.lb7 = Label(self.root, text='表单')
        self.lb7.place(relx=0.01, rely=0.5, relwidth=0.1, relheight=0.05)

        self.lb8 = Label(self.root, text='IP地址')
        self.lb8.place(relx=0.51, rely=0.1, relwidth=0.1, relheight=0.05)
        self.lb9 = Label(self.root, text='用户名')
        self.lb9.place(relx=0.51, rely=0.2, relwidth=0.1, relheight=0.05)
        self.lb10 = Label(self.root, text='密码')
        self.lb10.place(relx=0.51, rely=0.3, relwidth=0.1, relheight=0.05)
        self.lb11 = Label(self.root, text='数据库')
        self.lb11.place(relx=0.51, rely=0.4, relwidth=0.1, relheight=0.05)

        self.inp1 = Entry(self.root)
        self.inp1.place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.05)
        self.inp2 = Entry(self.root)
        self.inp2.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.05)
        self.inp3 = Entry(self.root)
        self.inp3.place(relx=0.1, rely=0.3, relwidth=0.3, relheight=0.05)
        self.inp4 = Entry(self.root)
        self.inp4.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.05)
        self.inp9 = Entry(self.root)
        self.inp9.place(relx=0.1, rely=0.5, relwidth=0.3, relheight=0.05)

        self.inp5 = Entry(self.root)
        self.inp5.place(relx=0.6, rely=0.1, relwidth=0.3, relheight=0.05)
        self.inp6 = Entry(self.root)
        self.inp6.place(relx=0.6, rely=0.2, relwidth=0.3, relheight=0.05)
        self.inp7 = Entry(self.root)
        self.inp7.place(relx=0.6, rely=0.3, relwidth=0.3, relheight=0.05)
        self.inp8 = Entry(self.root)
        self.inp8.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.05)

        # 方法一导出直接调用 run1()
        self.btn1 = Button(self.root, text='导出指定表', command=self.run1)
        self.btn1.place(relx=0.07, rely=0.6, relwidth=0.15, relheight=0.05)

        # 方法二导入直接调用 run2()
        self.btn2 = Button(self.root, text='导入', command=self.run2)
        self.btn2.place(relx=0.65, rely=0.48, relwidth=0.15, relheight=0.05)

        # 方法一导出直接调用 run1()
        self.btn3 = Button(self.root, text='导出所有表', command=self.run3)
        self.btn3.place(relx=0.27, rely=0.6, relwidth=0.15, relheight=0.05)

        # 在窗体垂直自上而下位置60%处起，布局相对窗体高度40%高的文本框
        self.txt = Text(self.root)
        self.txt.place(rely=0.7, relwidth=1, relheight=0.3)

        self.root.mainloop()

    def run1(self):
        host = str(self.inp1.get())
        user = str(self.inp2.get())
        pwd = str(self.inp3.get())
        dbname = str(self.inp4.get())
        tablename = str(self.inp9.get())
        ex = ep.ExportOracle(host, user, pwd, dbname)
        s = ex.export_oracle_data(tablename)
        self.txt.insert(END, s)  # 追加显示运算结果
        # inp1.delete(0, END)  # 清空输入
        # inp2.delete(0, END)  # 清空输入
        # inp3.delete(0, END)  # 清空输入
        # inp4.delete(0, END)  # 清空输入
        self.inp9.delete(0, END)  # 清空输入

    def run2(self):
        host = str(self.inp5.get())
        user = str(self.inp6.get())
        pwd = str(self.inp7.get())
        dbname = str(self.inp8.get())
        im = id.ImportMysql(host, user, pwd, dbname)
        s = im.excel2mysql()
        self.txt.insert(END, s)  # 追加显示运算结果
        # inp5.delete(0, END)  # 清空输入
        # inp6.delete(0, END)  # 清空输入
        # inp7.delete(0, END)  # 清空输入
        # inp8.delete(0, END)  # 清空输入

    def run3(self):
        host = str(self.inp1.get())
        user = str(self.inp2.get())
        pwd = str(self.inp3.get())
        dbname = str(self.inp4.get())
        ex = ep.ExportOracle(host, user, pwd, dbname)
        s = ex.export_all_oracle_data()
        self.txt.insert(END, s)  # 追加显示运算结果


a=Transdata()