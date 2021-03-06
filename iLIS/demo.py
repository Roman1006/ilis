# -*- coding: utf-8 -*-
# @Time : 2020-12-28 19:19
# @Author : Roman
# @FileName : demo.py
# @Email : 13883575239@163.com
# @Software: PyCharm
import unittest
import os
from iLIS import readconf
from iLIS.common.Log import MyLog
from openpyxl import load_workbook
local_readConfig =  readconf.Read_conf()

def test_01_a():
    cell_list = []
    for cell_ord in range(ord("A"), ord("Q") + 1):
        cell_name = cell_ord
        # print(chr(cell_name))
        value = local_readConfig.get_case_cellname(chr(cell_name))
        print(value)
        cell_list.append(value)
    print(cell_list)
test_01_a()