# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-05-12 20:04:54
@LastEditTime: 2020-11-27 09:19:53
@LastEditors: HuangJingCan
@Description: 用户相关
"""
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.seven_model import *

from seven_cloudapp.models.db_models.app.app_info_model import *
from seven_cloudapp.models.db_models.login.login_log_model import *
from seven_cloudapp.models.db_models.user.user_info_model import *
from seven_cloudapp.models.db_models.machine.machine_value_model import *
from seven_cloudapp.models.db_models.user.user_blacklist_model import *

from seven_cloudapp.libs.customize.seven import *


class LoginHandler(SevenBaseHandler):
    """
    @description: 登录处理
    """
    @filter_check_params("open_id")
    def get_async(self):
        """
        @description: 登录日志入库
        @param open_id：用户唯一标识
        @param user_nick：用户昵称
        @return: 
        @last_editors: HuangJingCan
        """
        open_id = self.get_taobao_param().open_id
        user_nick = self.get_taobao_param().user_nick
        source_app_id = self.get_taobao_param().source_app_id

        request_params = str(self.request_params)

        if user_nick == "":
            return self.reponse_json_success()

        login_log_model = LoginLogModel()
        login_log = login_log_model.get_entity("open_id=%s", params=open_id)

        is_add = False
        if not login_log:
            is_add = True
            login_log = LoginLog()

        login_log.open_id = open_id
        login_log.user_nick = user_nick
        if user_nick.__contains__(":"):
            login_log.store_user_nick = user_nick.split(":")[0]
            login_log.is_master = 0
        else:
            login_log.store_user_nick = user_nick
            login_log.is_master = 1
        login_log.request_params = request_params
        login_log.modify_date = self.get_now_datetime()

        if is_add:
            login_log.create_date = login_log.modify_date
            login_log.id = login_log_model.add_entity(login_log)
        else:
            login_log_model.update_entity(login_log)

        self.reponse_json_success()


class UserStatusHandler(SevenBaseHandler):
    """
    @description: 更新用户状态
    """
    @filter_check_params("userid,user_state")
    def get_async(self):
        """
        @description: 更新用户状态
        @param userid：用户id
        @param user_state：用户状态
        @return: reponse_json_success
        @last_editors: HuangJingCan
        """
        user_id = int(self.get_param("userid"), 0)
        user_state = int(self.get_param("user_state"), 0)
        modify_date = self.get_now_datetime()
        relieve_date = self.get_now_datetime()

        if user_id <= 0:
            return self.reponse_json_error("error", "找不到用户!")

        user_model = UserInfoModel()
        user_info = user_model.get_entity_by_id(user_id)
        if not user_info:
            return self.reponse_json_error("error", "找不到用户!")

        user_model.update_table("user_state=%s,modify_date=%s,relieve_date=%s", "id=%s", [user_state, modify_date, relieve_date, user_id])

        if user_state == 1:
            if user_info.user_state == 1:
                return self.reponse_json_error("error", "该用户已是黑名单!")

            #添加到用户黑名单管理表
            user_blacklist = UserBlacklist()
            user_blacklist.app_id = user_info.app_id
            user_blacklist.act_id = user_info.act_id
            user_blacklist.open_id = user_info.open_id
            user_blacklist.user_nick = user_info.user_nick
            user_blacklist.black_type = 2
            user_blacklist.refund_order_data = []
            user_blacklist.create_date = self.get_now_datetime()
            UserBlacklistModel().add_entity(user_blacklist)

        self.reponse_json_success()


class UserListHandler(SevenBaseHandler):
    """
    @description: 用户列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 用户列表
        @param page_index：页索引
        @param page_size：页大小
        @param act_id：活动id
        @param user_nick：用户昵称
        @return PageInfo
        @last_editors: HuangJingCan
        """
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))
        act_id = int(self.get_param("act_id", 0))
        user_nick = self.get_param("nick_name")
        condition = "act_id=%s"
        params = [act_id]

        if user_nick:
            condition += " AND user_nick=%s"
            params.append(user_nick)

        page_list, total = UserInfoModel().get_dict_page_list("*", page_index, page_size, condition, order_by="id desc", params=params)

        page_info = PageInfo(page_index, page_size, total, page_list)

        self.reponse_json_success(page_info)


class UserBlackStatusHandler(SevenBaseHandler):
    """
    docstring 黑名单状态管理
    """
    @filter_check_params("black_id,audit_status")
    def get_async(self):
        """
        @description: 黑名单状态管理
        @param black_id：用户黑名单管理id
        @param audit_status：审核状态(0黑名单1申请中2同意3拒绝)
        @return: reponse_json_success
        @last_editors: HuangJingCan
        """
        black_id = int(self.get_param("black_id", 0))
        audit_status = int(self.get_param("audit_status", 0))
        audit_date = self.get_now_datetime()

        if black_id <= 0:
            return self.reponse_json_error("error", "找不到该条记录!")

        user_blacklist_model = UserBlacklistModel()
        black_info = user_blacklist_model.get_entity_by_id(black_id)
        if not black_info:
            return self.reponse_json_error("error", "找不到该条记录!")

        user_blacklist_model.update_table("audit_status=%s,audit_date=%s", "id=%s", [audit_status, audit_date, black_id])

        if audit_status == 2:
            user_info_model = UserInfoModel()
            userInfo = user_info_model.get_entity("act_id=%s and open_id=%s", params=[black_info.act_id, black_info.open_id])
            if not userInfo:
                return self.reponse_json_error("error", "找不到用户!")

            userInfo.user_state = 0
            userInfo.modify_date = audit_date
            userInfo.relieve_date = audit_date
            user_info_model.update_entity(userInfo)

        self.reponse_json_success()


class UserBlackListHandler(SevenBaseHandler):
    """
    获取黑名单管理列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 获取黑名单管理列表
        @param act_id：act_id
        @return: list
        @last_editors: HuangJingCan
        """
        act_id = int(self.get_param("act_id", 0))
        audit_status = int(self.get_param("audit_status", -1))
        user_nick = self.get_param("nick_name")
        create_date_start = self.get_param("create_date_start")
        create_date_end = self.get_param("create_date_end")

        if act_id <= 0:
            return self.reponse_json_error_params()

        condition = "act_id=%s"
        params = [act_id]

        if audit_status >= 0:
            condition += " AND audit_status=%s"
            params.append(audit_status)
        if user_nick:
            condition += " AND user_nick=%s"
            params.append(user_nick)
        if create_date_start:
            condition += " AND create_date>=%s"
            params.append(create_date_start)
        if create_date_end:
            condition += " AND create_date<=%s"
            params.append(create_date_end)

        user_black_dict_list = UserBlacklistModel().get_dict_list(condition, order_by="create_date desc", params=params)

        for user_black in user_black_dict_list:
            user_black["refund_order_data"] = json.loads(user_black["refund_order_data"]) if user_black["refund_order_data"] else []

        self.reponse_json_success(user_black_dict_list)