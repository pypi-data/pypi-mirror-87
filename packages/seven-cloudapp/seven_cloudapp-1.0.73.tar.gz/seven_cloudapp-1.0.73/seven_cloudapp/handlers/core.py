# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-05-26 14:45:44
@LastEditTime: 2020-11-04 17:26:35
@LastEditors: HuangJingCan
@Description: 通用Handler
"""
from seven_cloudapp.handlers.seven_base import *


class IndexHandler(SevenBaseHandler):
    """
    @description: 默认页
    """
    def get_async(self):
        """
        @description: 默认页
        @param 
        @return 字符串
        @last_editors: HuangJingCan
        """
        self.write(config.get_value("project_name") + "_api")