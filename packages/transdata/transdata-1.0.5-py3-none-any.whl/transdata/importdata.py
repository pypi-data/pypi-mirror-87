import pandas as pd
import numpy as np
import pymysql
import os


class ImportMysql():
    def __init__(self):

        host = input("请输入数据库服务器IP：")
        user = input("请输入您的数据库用户名：")
        pwd = input("请输入您的用户密码：")
        dbname = input("请输入您想连接的数据库名称：")
        self.host = str(host)
        self.user = str(user)
        self.pwd = str(pwd)
        self.dbname = str(dbname)
        try:
            connection = pymysql.connect(self.host, self.user, self.pwd, self.dbname)
            connection.autocommit(1)
            self.cursor = connection.cursor()
            print('数据库连接成功啦！！！')
        except Exception as e:
            print('警告警告！！！数据库连接信息输入错误，请重新输入！！！')
            print(e)

    def create_table_sql(self):
        path = os.getcwd()
        files = os.listdir(path)
        for file in files:
            if file.split('.')[-1] in ['xls']:
                struc = pd.read_excel(file)
                train_data = np.array(struc)  # np.ndarray()
                stru_list = train_data.tolist()  # list
                # columns = df.columns.tolist()
                # 添加id 制动递增主键模式
                make_table = []
                for item in stru_list:
                    if 'INT' in str(item[1]):
                        char = item[0] + ' INT'
                    elif 'NUMBER' in str(item[1]):
                        if item[3] == '0':
                            char = item[0] + f' INT({int(item[2])})'
                        elif item[3] != '0' and item[3] != 'None':
                            char = item[0] + f' float{int(item[2]), int(item[3])}'
                        elif item[2] == 'None':
                            char = item[0] + f' INT'

                    elif 'VARCHAR2' in str(item[1]):
                        char = item[0] + f' varchar({int(item[4])})'
                    elif 'DATE' in str(item[1]):
                        char = item[0] + ' DATETIME'
                    make_table.append(char)
                os.remove(file)
                print('已删除' + path + '\\' + file)
                return ','.join(make_table)

    # excel格式输入 mysql 中
    def excel2mysql(self):
        path = os.getcwd()
        files = os.listdir(path)
        for file in files:
            if file.split('.')[-1] in ['xlsx']:
                filename = file.split('.')[0]
                data_xls = pd.io.excel.ExcelFile(file)
                for name in data_xls.sheet_names:
                    df = pd.read_excel(data_xls, sheet_name=name)
                    self.cursor.execute('DROP TABLE IF EXISTS {}'.format(name))
                    self.cursor.execute('CREATE TABLE {}({})'.format(name, self.create_table_sql()))
                    # print('%s表单创建成功！！！' % name)
                    # 提取数据转list 这里有与pandas时间模式无法写入因此换成str 此时mysql上格式已经设置完成
                    # df['HIREDATE'] = df['HIREDATE'].astype('str')
                    sb = ','.join(['%s' % df.columns[y] for y in range(len(df.columns))])
                    z = ','.join('%s' for y in range(len(df.columns)))
                    df = df.where(df.notnull(), None)  # 将列表内的Nan值换为None
                    values = df.values.tolist()
                    sql = f"INSERT INTO {name}({sb}) VALUES ({z})"
                    # 批量导入数据库，executemany批量操作 插入数据 批量操作比逐个操作速度快很多
                    self.cursor.executemany(sql, values)
                    # cursor.executemany('INSERT INTO {} ({}) VALUES ({})'.format(table_name, sb), values)
                    print("恭喜！！！数据导入mysql成功！！！")
                os.remove(filename + '.xlsx')
                print('已删除' + path + '\\' + filename + '.xlsx')


# ad = ImportMysql()
# ad.excel2mysql()
