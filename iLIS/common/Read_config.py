# -*- coding: utf-8 -*-
# @Time : 2020-12-10 10:51
# @Author : Roman
# @FileName : Read_config.py
# @Email : 13883575239@163.com
# @Software: PyCharm

import time
from iLIS import readconf
from iLIS.common.Log import MyLog


local_readConfig =  readconf.Read_conf()

class Readconfig:
    def __init__(self):
        self.pay_need = local_readConfig.get_pay_msg("pay_need")
        self.pay_nneed = local_readConfig.get_pay_msg("pay_nneed")

        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
    # @classmethod
    def read_config(self):
        """明确收费委托类型"""
        pay_need_list = []
        pay_nneed_list = []
        # self.logger.info("================在配置文件中查找是否收费的类型名称===============")
        for i in str(self.pay_need).split('/'):
            pay_need_list.append(i)
        # print(pay_need_list)
        for i in str(self.pay_nneed).split('/'):
            pay_nneed_list.append(i)
        # print(pay_nneed_list)
        return pay_need_list,pay_nneed_list
    def red_excel_cell(self):
        cell_list = []
        for cell_ord in range(ord("A"), ord("Q") + 1):
            cell_name = cell_ord
            value = local_readConfig.get_case_cellname(chr(cell_name))
            cell_list.append(value)
        return cell_list
    def red_excel_cell_value(self,value):
        value = local_readConfig.get_case_cellname(value)
        return value

