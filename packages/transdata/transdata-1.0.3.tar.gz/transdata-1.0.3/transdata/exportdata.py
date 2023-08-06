import cx_Oracle
import xlwt
import os

path = os.getcwd()

class ExportData():
    def __init__(self, host, user, pwd, dbname):
        '''print('欢迎客官莅临！！！撒花！！！')
        host = input("请输入数据库服务器IP：")
        user = input("请输入您的数据库用户名：")
        pwd = input("请输入您的用户密码：")
        dbname = input("请输入您想连接的数据库名称：")'''
        self.host = str(host)
        self.user = str(user)
        self.pwd = str(pwd)
        self.dbname = str(dbname)
        try:
            moniter = cx_Oracle.makedsn(self.host, 1521, self.dbname)
            self.connection = cx_Oracle.connect(self.user, self.pwd, moniter)
        except Exception as e:
            print('警告警告！！！数据库连接信息输入错误，请重新输入！！！', e)
        self.cursor = self.connection.cursor()
        print('恭喜客官！数据库连接成功啦！！！')

    def export_all_oracle_data(self):
        try:
            sql = '''
                        select * from tab
                                      '''
            self.cursor.execute(sql)
            output_file = "%s.xlsx" % self.dbname
            workbook = xlwt.Workbook(output_file)
            print('客官稍等，数据正在导出······')
            for sheet in self.cursor:
                if not str(sheet[0]).startswith('BIN$'):  # skip recycle bin tables
                    tableName = str(sheet[0])
                    worksheet = workbook.add_sheet(tableName)
                    sql = '''
                                                select * from %s
                                              ''' % tableName
                    cursor = self.connection.cursor()
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    fields = cursor.description
                    for field in range(0, len(fields)):
                        # output.writerow(cols)
                        worksheet.write(0, field, fields[field][0])
                    for row_data in range(1, len(results) + 1):
                        for col in range(0, len(fields)):
                            # output.writerow(row_data)
                            worksheet.write(row_data, col, u'%s' % results[row_data - 1][col])
            workbook.save(output_file)
            print('恭喜客官成功导出' + output_file + '！！！！')
        except Exception as e:
            print('警告警告！！！数据导出失败！！！请重试！！！')
            print(e)

    def export_oracle_data(self, tablename):
        try:
            csv_file_dest = tablename + ".xlsx"
            sql = '''
                            select * from %s
                          ''' % tablename
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            fields = self.cursor.description
            workbook = xlwt.Workbook(csv_file_dest)
            worksheet = workbook.add_sheet(tablename)
            for field in range(0, len(fields)):
                worksheet.write(0, field, fields[field][0])
            for row_data in range(1, len(results) + 1):
                for col in range(0, len(fields)):
                    worksheet.write(row_data, col, u'%s' % results[row_data - 1][col])
            workbook.save(csv_file_dest)
            print(r'恭喜客官成功导出' +path+'\\'+csv_file_dest + '！！！！')

        except Exception as e:
            print('警告警告！！！数据导出失败！！！请重试！！！')
            print(e)
