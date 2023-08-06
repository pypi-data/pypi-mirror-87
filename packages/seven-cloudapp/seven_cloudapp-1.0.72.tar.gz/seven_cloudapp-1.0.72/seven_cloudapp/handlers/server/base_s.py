# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-05-24 17:26:33
@LastEditTime: 2020-11-23 16:37:25
@LastEditors: HuangJingCan
@Description: 基础信息相关
"""
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.db_models.base.base_info_model import *
from seven_cloudapp.models.db_models.app.app_info_model import *


class LeftNavigationHandler(SevenBaseHandler):
    """
    @description: 左侧导航栏
    """
    def get_async(self):
        """
        @description: 左侧导航栏
        @param {*}
        @return 字典
        @last_editors: HuangJingCan
        """
        base_info = BaseInfoModel().get_entity()
        if not base_info:
            return self.reponse_json_error("BaseInfoError", "基础信息出错")
        store_user_nick = self.get_taobao_param().user_nick.split(':')[0]
        if not store_user_nick:
            return self.reponse_json_error("Error", "对不起，请先授权登录")
        open_id = self.get_taobao_param().open_id
        if not open_id:
            return self.reponse_json_error("Error", "对不起，请先登录")
        open_id = self.get_taobao_param().open_id
        app_info = AppInfoModel().get_entity("store_user_nick=%s", params=store_user_nick)
        if not app_info:
            return self.reponse_json_error("AppInfoError", "App信息出错")

        # 左上角信息
        info = {}
        info["company"] = "天志互联"
        info["miniappName"] = config.get_value("project_name")
        info["logo"] = config.get_value("project_logo")

        # 左边底部菜单
        helper_info = {}
        helper_info["customer_service"] = "http://amos.alicdn.com/getcid.aw?v=2&uid=%E5%A4%A9%E5%BF%97%E4%BA%92%E8%81%94&site=cntaobao&s=1&groupid=0&charset=utf-8"
        helper_info["video_url"] = base_info.video_url
        helper_info["study_url"] = base_info.study_url
        helper_info["is_remind_phone"] = base_info.is_remind_phone
        helper_info["phone"] = app_info.app_telephone

        # 过期时间
        renew_info = {}
        renew_info["dead_date"] = app_info.expiration_date
        # if app_info.expiration_date == "1900-01-01 00:00:00":
        #     app_info.expiration_date = TimeHelper.add_days_by_format_time(self.get_now_datetime(), 10)
        renew_info["surplus_day"] = TimeHelper.difference_days(app_info.expiration_date, self.get_now_datetime())
        # renew_info["renew_prices"] = base_info.product_price

        data = {}
        data["app_info"] = info
        data["helper_info"] = helper_info
        data["renew_info"] = renew_info
        if base_info.product_price:
            data["renew_prices"] = ast.literal_eval(base_info.product_price)

        self.reponse_json_success(data)


class RightExplainHandler(SevenBaseHandler):
    """
    @description: 右侧各种教程和说明导航
    """
    def get_async(self):
        """
        @description: 右侧各种教程和说明导航
        @param {*}
        @return dict
        @last_editors: HuangJingCan
        """
        base_info = BaseInfoModel().get_entity()
        if not base_info:
            return self.reponse_json_error("BaseInfoError", "基础信息出错")

        data = []

        if base_info.course_strategy:
            data = ast.literal_eval(base_info.course_strategy)

        self.reponse_json_success(data)


class FriendLinkHandler(SevenBaseHandler):
    """
    @description: 获取友情链接
    """
    def get_async(self):
        """
        @description: 获取友情链接
        @param {*}
        @return list
        @last_editors: HuangJingCan
        """
        base_info = BaseInfoModel().get_entity()
        if not base_info:
            return self.reponse_json_error("BaseInfoError", "基础信息出错")

        data = []

        if base_info.friend_link:
            data = ast.literal_eval(base_info.friend_link)

        self.reponse_json_success(data)


class UpdateInfoHandler(SevenBaseHandler):
    """
    @description: 获取更新信息
    """
    @filter_check_params("app_id")
    def get_async(self):
        """
        @description: 获取更新信息
        @param app_id：app_id
        @return dict
        @last_editors: HuangJingCan
        """
        app_id = self.get_param("app_id")

        base_info = BaseInfoModel().get_entity()
        if not base_info:
            return self.reponse_json_error("BaseInfoError", "基础信息出错")
        app_info = AppInfoModel().get_entity("app_id=%s", params=app_id)
        if not app_info:
            return self.reponse_json_error("AppInfoError", "App信息出错")

        data = {}

        data["client_ver"] = base_info.client_ver
        data["server_ver"] = base_info.server_ver
        data["client_now_ver"] = app_info.template_ver
        data["update_function"] = []
        if base_info.update_function:
            data["update_function"] = ast.literal_eval(base_info.update_function)

        self.reponse_json_success(data)