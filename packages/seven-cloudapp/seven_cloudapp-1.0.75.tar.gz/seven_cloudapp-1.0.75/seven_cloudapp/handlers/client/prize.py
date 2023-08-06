# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-11-05 10:13:31
@LastEditTime: 2020-11-26 10:33:00
@LastEditors: HuangJingCan
@Description: 奖品相关
"""
from seven_cloudapp.handlers.top_base import *

from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.act.act_prize_model import *
from seven_cloudapp.models.db_models.pay.pay_order_model import *
from seven_cloudapp.models.db_models.prize.prize_roster_model import *
from seven_cloudapp.models.db_models.prize.prize_order_model import *

from seven_cloudapp.models.seven_model import PageInfo


class PrizeListHandler(SevenBaseHandler):
    """
    @description: 奖品列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description:  获取奖品列表
        @param act_id：活动id
        @param machine_id：机台id
        @param page_index：页索引
        @param page_size：页大小
        @return: 分页列表信息
        @last_editors: HuangJingCan
        """
        app_id = self.get_taobao_param().source_app_id
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))
        act_id = int(self.get_param("act_id", 0))
        machine_id = int(self.get_param("machine_id", 0))

        condition = "is_release=1 AND act_id=%s"
        params = [act_id]

        if machine_id > 0:
            condition += " AND machine_id=%s"
            params.append(machine_id)

        act_prize_page_list, total = ActPrizeModel().get_dict_page_list("*", page_index, page_size, condition, order_by="sort_index desc", params=params)

        for act_prize in act_prize_page_list:
            try:
                if act_prize["prize_detail"]:
                    act_prize["prize_detail"] = json.loads(act_prize["prize_detail"])
                else:
                    act_prize["prize_detail"] = []
            except Exception as ex:
                act_prize["prize_detail"] = []

        page_info = PageInfo(page_index, page_size, total, act_prize_page_list)

        self.reponse_json_success(page_info)


class SyncPayOrderHandler(TopBaseHandler):
    """
    @description: 用户支付订单提交（业务各自实现）
    """
    def get_async(self):
        """
        @description: 用户支付订单提交（业务各自实现）
        @param {*}
        @return {*}
        @last_editors: HuangJingCan
        """
        pass


class UserPrizeListHandler(SevenBaseHandler):
    """
    @description: 获取用户奖品列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 获取用户奖品列表
        @param act_id：活动id
        @return status：状态
        @param page_index：页索引
        @param page_size：页大小
        @return: 
        @last_editors: HuangJingCan
        """
        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id

        act_id = int(self.get_param("act_id", 0))
        status = int(self.get_param("status", 0))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))

        prize_roster_model = PrizeRosterModel()
        if status == 0:
            condition = "open_id=%s and act_id=%s and prize_order_id=0"
        else:
            condition = "open_id=%s and act_id=%s and prize_order_id>0"

        page_list, total = prize_roster_model.get_dict_page_list("*", page_index, page_size, condition, "", "create_date desc", [open_id, act_id])

        page_info = PageInfo(page_index, page_size, total, page_list)

        self.reponse_json_success(page_info)


class SubmitPrizeOrder(SevenBaseHandler):
    """
    @description: 奖品订单提交
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 奖品订单提交
        @param act_id：活动id
        @param login_token：登录令牌
        @param real_name：用户名
        @param telephone：联系电话
        @param province：所在省
        @param city：所在市
        @param county：所在区
        @param street：所在街道
        @param address：收货地址
        @return 
        @last_editors: HuangJingCan
        """
        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id

        act_id = int(self.get_param("act_id", 0))
        login_token = self.get_param("login_token")
        real_name = self.get_param("real_name")
        telephone = self.get_param("telephone")
        province = self.get_param("province")
        city = self.get_param("city")
        county = self.get_param("county")
        street = self.get_param("street")
        address = self.get_param("address")

        user_info = UserInfoModel().get_entity("act_id=%s and open_id=%s", params=[act_id, open_id])
        if not user_info:
            return self.reponse_json_error("NoUser", "对不起，用户不存在")
        if user_info.user_state == 1:
            return self.reponse_json_error("UserBlock", "对不起，你是黑名单用户,无法提交订单")
        if user_info.login_token != login_token:
            return self.reponse_json_error("ErrorLoginToken", "对不起，帐号已在另一台设备登录,当前无法提交订单")

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s and is_del=0 and is_release=1", params=act_id)
        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，活动不存在")

        prize_roster_model = PrizeRosterModel()
        prize_roster_count = prize_roster_model.get_total("act_id=%s and open_id=%s and prize_order_id=0", params=[act_id, open_id])
        if prize_roster_count == 0:
            return self.reponse_json_error("NoNeedSubmitPrize", "当前没有未提交订单的奖品")

        prize_order_model = PrizeOrderModel()
        prize_order = PrizeOrder()
        prize_order.app_id = app_id
        prize_order.open_id = open_id
        prize_order.act_id = act_id
        prize_order.user_nick = user_info.user_nick
        prize_order.real_name = real_name
        prize_order.telephone = telephone
        prize_order.province = province
        prize_order.city = city
        prize_order.county = county
        prize_order.street = street
        prize_order.adress = address
        prize_order.create_date = self.get_now_datetime()
        prize_order.modify_date = self.get_now_datetime()
        prize_order.order_no = self.create_order_id()

        prize_order.id = prize_order_model.add_entity(prize_order)

        prize_roster_model.update_table("prize_order_id=%s,prize_order_no=%s", "act_id=%s and open_id=%s and prize_order_id=0", params=[prize_order.id, prize_order.order_no, act_id, open_id])

        self.reponse_json_success()


class PrizeOrderHandler(SevenBaseHandler):
    """
    @description: 用户订单列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 用户订单列表
        @param act_id：活动id
        @param page_index：页索引
        @param page_size：页大小
        @return: 
        @last_editors: HuangJingCan
        """
        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id

        act_id = int(self.get_param("act_id", 0))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))

        prize_order_model = PrizeOrderModel()
        prize_roster_model = PrizeRosterModel()
        prize_order_list_dict, total = prize_order_model.get_dict_page_list("*", page_index, page_size, "open_id=%s and act_id=%s ", "", "create_date desc", [open_id, act_id])
        if prize_order_list_dict:
            prize_order_id_list = [i["id"] for i in prize_order_list_dict]
            prize_order_ids = str(prize_order_id_list).strip('[').strip(']')
            prize_roster_list_dict = prize_roster_model.get_dict_list("prize_order_id in (" + prize_order_ids + ")")
            for i in range(len(prize_order_list_dict)):
                prize_order_list_dict[i]["prize_order_list"] = [prize_roster for prize_roster in prize_roster_list_dict if prize_order_list_dict[i]["id"] == prize_roster["prize_order_id"]]

        page_info = PageInfo(page_index, page_size, total, prize_order_list_dict)

        self.reponse_json_success(page_info)


class RosterNoticeHandler(SevenBaseHandler):
    """
    @description: 中奖通告
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 中奖通告
        @param act_id：活动id
        @return 列表
        @last_editors: HuangJingCan
        """
        act_id = int(self.get_param("act_id", 0))

        prize_roster_list_dict = PrizeRosterModel().get_dict_list("act_id=%s", order_by="create_date desc", limit="20", params=act_id)

        self.reponse_json_success(prize_roster_list_dict)