# -*- coding:utf-8 -*-
"""
作者：jiangshuo
日期：2020年11月26日
"""
import cx_Oracle
import os


# 创建数据库连接
class TestOracle:
    def __init__(self, user, pwd, ip, port, sid):
        self.connect = cx_Oracle.connect(user+"/"+pwd+"@"+ip+":"+port+"/"+sid, mode=cx_Oracle.SYSDBA)
        self.cursor = self.connect.cursor()

    def disconnect(self):
        self.cursor.close()
        self.connect.close()

    def sql_grant_character(self, k_lie, privilege, e_lie):   # 可选变量
        sql_grant = f'''
        select 'grant {privilege} on '||a.owner|| '.' ||a.table_name|| ' to {e_lie} with grant option;' txt 
        from dba_tab_privs a where grantee ='{k_lie}'
        '''
        try:
            a = self.cursor.execute(sql_grant)  # 执行
            rs = self.cursor.fetchall()   # 获得运行结果
            for ii in rs:
                print(ii[0])
            self.connect.commit()   # 提交
        except Exception as e:  # 例外
            print(e)
        return rs
