# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-05-19 11:33:16
@LastEditTime: 2020-12-08 14:23:43
@LastEditors: HuangJingCan
@Description: 用户处理
"""
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.seven_model import PageInfo
from seven_cloudapp.models.behavior_model import *

from seven_cloudapp.models.db_models.user.user_info_model import *
from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.machine.machine_info_model import *
from seven_cloudapp.models.db_models.machine.machine_value_model import *

from seven_cloudapp.libs.customize.seven import *


class LoginHandler(SevenBaseHandler):
    """
    @description: 登录处理
    """
    @filter_check_params("act_id,open_id")
    def get_async(self):
        """
        @description: 登录日志入库
        @param owner_open_id：应用拥有者唯一标识
        @param act_id：活动id
        @return: dict
        @last_editors: HuangJingCan
        """
        open_id = self.get_taobao_param().open_id
        user_nick = self.get_taobao_param().user_nick
        app_id = self.get_taobao_param().source_app_id
        owner_open_id = self.get_param("owner_open_id")
        act_id = int(self.get_param("act_id", 0))

        user_info_model = UserInfoModel()
        user_info = user_info_model.get_entity("act_id=%s and open_id=%s", params=[act_id, open_id])

        act_info = ActInfoModel().get_entity("id=%s", params=act_id)
        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，活动不存在")

        if not user_info:
            user_info = UserInfo()
            user_info.open_id = open_id
            user_info.act_id = act_id
            user_info.app_id = app_id
            user_info.is_new = 1
            user_info.user_nick = user_nick
            user_info.create_date = self.get_now_datetime()
            user_info.modify_date = self.get_now_datetime()
            user_info.login_token = SevenHelper.get_random(16, 1)
            user_info.id = user_info_model.add_entity(user_info)
        else:
            if user_nick:
                user_info.user_nick = user_nick
            user_info.modify_date = self.get_now_datetime()
            user_info.login_token = SevenHelper.get_random(16, 1)
            user_info.is_new = 0
            user_info_model.update_entity(user_info, "modify_date,login_token,is_new,user_nick")

        behavior_model = BehaviorModel()
        # 访问次数
        behavior_model.report_behavior_log(app_id, act_id, open_id, owner_open_id, 'VisitCountEveryDay', 1)
        # 访问人数
        behavior_model.report_behavior_log(app_id, act_id, open_id, owner_open_id, 'VisitManCountEveryDay', 1)
        if user_info.is_new == 1:
            # 新增用户数
            behavior_model.report_behavior_log(app_id, act_id, open_id, owner_open_id, 'VisitManCountEveryDayIncrease', 1)

        self.reponse_json_success(user_info)


class LoginByMachineHandler(SevenBaseHandler):
    """
    @description: 登录处理（包含机台信息）
    """
    @filter_check_params("act_id,open_id")
    def get_async(self):
        """
        @description: 登录日志入库
        @param owner_open_id：应用拥有者唯一标识
        @param act_id：活动id
        @return: dict
        @last_editors: HuangJingCan
        """
        open_id = self.get_taobao_param().open_id
        user_nick = self.get_taobao_param().user_nick
        app_id = self.get_taobao_param().source_app_id
        owner_open_id = self.get_param("owner_open_id")
        act_id = int(self.get_param("act_id", 0))

        user_info_model = UserInfoModel()
        user_info = user_info_model.get_entity("act_id=%s and open_id=%s", params=[act_id, open_id])

        act_info = ActInfoModel().get_entity("id=%s", params=act_id)
        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，活动不存在")

        machine_info_model = MachineInfoModel()
        machine_info_list = machine_info_model.get_list("act_id=%s", params=[act_id])
        if not machine_info_list:
            return self.reponse_json_error("NoMachine", "对不起，机台不存在")

        if not user_info:
            user_info = UserInfo()
            user_info.open_id = open_id
            user_info.act_id = act_id
            user_info.app_id = app_id
            user_info.is_new = 1
            user_info.user_nick = user_nick
            user_info.create_date = self.get_now_datetime()
            user_info.modify_date = self.get_now_datetime()
            user_info.login_token = SevenHelper.get_random(16, 1)
            user_info.id = user_info_model.add_entity(user_info)
        else:
            if user_nick:
                user_info.user_nick = user_nick
            user_info.modify_date = self.get_now_datetime()
            user_info.login_token = SevenHelper.get_random(16, 1)
            user_info.is_new = 0
            user_info_model.update_entity(user_info, "modify_date,login_token,is_new,user_nick")

        machine_value_model = MachineValueModel()
        machine_value_list = machine_value_model.get_dict_list("open_id=%s", params=open_id)
        user_info_dict = user_info.__dict__
        user_info_dict["machine_value_list"] = machine_value_list

        behavior_model = BehaviorModel()
        # 访问次数
        behavior_model.report_behavior(app_id, act_id, open_id, owner_open_id, 'VisitCountEveryDay', 1)
        # 访问人数
        behavior_model.report_behavior(app_id, act_id, open_id, owner_open_id, 'VisitManCountEveryDay', 1)
        if user_info.is_new == 1:
            # 新增用户数
            behavior_model.report_behavior(app_id, act_id, open_id, owner_open_id, 'VisitManCountEveryDayIncrease', 1)

        self.reponse_json_success(user_info_dict)


class UserHandler(SevenBaseHandler):
    """
    @description: 更新用户信息
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 更新用户信息
        @param avatar：头像
        @param act_id：活动id
        @return: 
        @last_editors: HuangJingCan
        """
        try:
            open_id = self.get_taobao_param().open_id
            user_nick = self.get_taobao_param().user_nick
            source_app_id = self.get_taobao_param().source_app_id
            avatar = self.get_param("avatar")
            act_id = int(self.get_param("act_id", 0))

            user_info_model = UserInfoModel()
            user_info = user_info_model.get_entity("act_id=%s and open_id=%s", params=[act_id, open_id])
            if not user_info:
                return self.reponse_json_error("NoUser", "对不起，用户不存在")

            if user_nick:
                user_info.user_nick = user_nick
            user_info.avatar = avatar
            user_info.is_auth = 1
            user_info.modify_date = self.get_now_datetime()
            user_info_model.update_entity(user_info)

            self.reponse_json_success("更新成功")
        except Exception as ex:
            self.reponse_json_error("Error", "更新失败")