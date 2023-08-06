# -*- coding:utf-8 -*-
"""
作者：jiangshuo
日期：2020年11月27日
"""
import grant_user.grant.grant_select as grant
import xlrd
import sys
import importlib
import re
importlib.reload(sys)


def name_judge(row_name, col_name):
    for d in range(0, len(row_name)):
        if row_name[d] == col_name:
            col = d
            return col


def extract_character(k_lie_value):
    # 以“、”为分界点对字符串按照用户进行切片
    ss = k_lie_value.split('、')
    # 提取各切片中的用户名（数字、英文）
    privilege_list = []
    for m in ss:
        character = re.sub(u"([^\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", m)
        privilege_list.append(character)
    print(privilege_list)

    return privilege_list


def write(sql_grant1, save_path1):
    f = open(save_path1, 'a+')
    f.write(sql_grant1)
    f.close()
    return sql_grant1


def read_list():
    # 获取workbook中所有的sheet
    sheets = source.sheets()
    print(sheets)
    sheet_names = source.sheet_names()
    # 循环遍历所有sheet
    print("一共有%s个sheet" % len(sheets))
    privilege = 'select'
    port = '1521'
    for i in range(len(sheets)):   # 有几个工作表
        table = source.sheet_by_index(i)   # 通过索引获取表格
        sheet_name = sheet_names[i]   # 第i个sheet表的名称
        print("第%s个sheet表: %s" % ((i+1), sheet_name))       # 第几个sheet
        row_name = table.row_values(0)   # 获取第一行内容
        a = name_judge(row_name, '用户名')
        elie_value = table.col_values(a)   # 获取第i个表用户名
        b = name_judge(row_name, '用户权限说明 ')
        k_lie_value = table.col_values(b)   # 获取第i个表用户权限
        c = name_judge(row_name, 'IP地址')
        ip_value = table.col_values(c)   # 获取第i个表ip地址
        ips = ip_value[1]
        d = name_judge(row_name, '实例名')
        sid_value = table.col_values(d)   # 获取第i个表sid
        sids = sid_value[1]
        characters = extract_character(k_lie_value[1])   # 用户权限字段提取
        h_lie_value = characters
        for j in range(1, len(elie_value)):
            e_lie = elie_value[j]
            print(e_lie)
            for k in range(len(h_lie_value)):
                h_lie = h_lie_value[k]
                test_oracle = grant.TestOracle(user, password, ips, port, sids)
                # sql_grant = test_oracle.sql_grant_character('SYS', privilege, e_lie)
                sql_grant = test_oracle.sql_grant_character(h_lie, privilege, e_lie)
                # print(sql_grant.rs)
                for jj in sql_grant:
                    print(jj[0])
                    txt = write(jj[0]+'\n', save_path)

    print('SQL脚本已被成功保存在%s文件中' % save_path)


def main():
    path_name = input('请输入Excel表格所在的路径和名称：')
    # path_name = r"C:\Users\jiangshuo\Desktop\客服中心申请数据库实名账户.xls"
    global source, user, password, save_path
    source = xlrd.open_workbook(r"%s" % path_name)
    user = input('请输入管理员用户名：')
    password = input('请输入管理员用户密码：')
    save_path = input('请输入SQL脚本的保存路径及名称：')
    # save_path = 'E:\test.txt'

    json_data = read_list()

if __name__ == '__main__':
    main()