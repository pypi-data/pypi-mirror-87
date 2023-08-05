# -*- coding: utf-8 -*-
"""
@Author: CaiYouBin
@Date: 2020-05-26 15:26:32
@LastEditTime: 2020-11-24 17:25:31
@LastEditors: HuangJingCan
@Description: 客户端活动处理
"""
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.seven_model import PageInfo

from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.app.app_info_model import *


class ActInfoHandler(SevenBaseHandler):
    """
    @description: 获取活动信息
    """
    def get_async(self):
        """
        @description: 获取活动信息
        @param act_id：活动id
        @return: 字典
        @last_editors: HuangJingCan
        """
        act_id = int(self.get_param("act_id", 0))

        app_id = self.get_taobao_param().source_app_id

        app_info_model = AppInfoModel()
        app_info = app_info_model.get_entity("app_id=%s", params=app_id)
        if not app_info:
            return self.reponse_json_error("NoApp", "对不起，找不到该小程序")

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s", params=act_id)
        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，找不到该活动")

        act_info.store_id = app_info.store_id
        act_info.store_name = app_info.store_name

        self.reponse_json_success(act_info)