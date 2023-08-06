# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-11-05 10:03:55
@LastEditTime: 2020-11-24 17:25:11
@LastEditors: HuangJingCan
@Description: 机台相关
"""
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.seven_model import PageInfo

from seven_cloudapp.models.db_models.machine.machine_info_model import *


class MachinieListHandler(SevenBaseHandler):
    """
    @description: 机台列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 获取机台列表
        @param act_id：活动id
        @param page_index：页索引
        @param page_size：页大小
        @return: 分页列表信息
        @last_editors: HuangJingCan
        """
        app_id = self.get_taobao_param().source_app_id
        act_id = int(self.get_param("act_id", "0"))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))

        machine_info_model = MachineInfoModel()
        condition = "act_id=%s AND app_id=%s AND is_release=1"
        machine_info_page_list, total = machine_info_model.get_dict_page_list("*", page_index, page_size, condition, order_by="sort_index desc", params=[act_id, app_id])

        page_info = PageInfo(page_index, page_size, total, machine_info_page_list)

        self.reponse_json_success(page_info)