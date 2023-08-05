# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-06-02 13:44:17
@LastEditTime: 2020-11-27 16:00:52
@LastEditors: HuangJingCan
@Description: 奖品相关
"""
from seven_cloudapp.handlers.top_base import *

from seven_cloudapp.models.enum import *
from seven_cloudapp.models.seven_model import *
from seven_cloudapp.models.throw_model import *

from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.act.act_prize_model import *
from seven_cloudapp.models.db_models.prize.prize_roster_model import *
from seven_cloudapp.models.db_models.throw.throw_goods_model import *


class PrizeListHandler(SevenBaseHandler):
    """
    @description: 奖品列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 奖品列表
        @param page_index：页索引
        @param page_size：页大小
        @param act_id：活动id
        @param ascription_type：奖品归属（0-活动奖品1-任务奖品）
        @return: PageInfo
        @last_editors: HuangJingCan
        """
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 10))
        act_id = int(self.get_param("act_id", 0))
        ascription_type = int(self.get_param("ascription_type", 0))

        condition = "act_id=%s"
        order_by = "sort_index desc"
        params = [act_id]

        if act_id <= 0:
            return self.reponse_json_error_params()

        if ascription_type == 1:
            condition += " AND ascription_type=1"

        act_prize_model = ActPrizeModel()

        prize_all_count = 0
        prize_surplus_count = 0
        prize_lottery_count = 0
        sum_probability = {'probability': 0}

        if ascription_type == 0:
            # 奖品总件数
            prize_all_count = act_prize_model.get_total("act_id=%s", params=act_id)
            # 库存不足奖品件数
            prize_surplus_count = act_prize_model.get_total("act_id=%s AND surplus=0", params=act_id)
            # 可被抽中奖品件数
            prize_lottery_count = act_prize_model.get_total("act_id=%s AND probability>0 AND surplus>0 AND is_release=1", params=act_id)
            #奖品总权重
            sum_probability = act_prize_model.get_dict("act_id=%s and is_release=1", field="sum(probability) as probability", params=act_id)

        page_list, total = act_prize_model.get_dict_page_list("*", page_index, page_size, condition, "", order_by, act_id)

        for page in page_list:
            page["prize_detail"] = ast.literal_eval(page["prize_detail"]) if page["prize_detail"] else []
            page["goods_code_list"] = ast.literal_eval(page["goods_code_list"]) if page["goods_code_list"] else []
            page["sku_detail"] = ast.literal_eval(page["sku_detail"]) if page["sku_detail"] else []

        page_info = PageInfo(page_index, page_size, total, page_list)

        page_info.prize_all_count = prize_all_count
        page_info.prize_surplus_count = prize_surplus_count
        page_info.prize_lottery_count = prize_lottery_count
        page_info.prize_sum_probability = int(sum_probability["probability"]) if sum_probability["probability"] else 0

        self.reponse_json_success(page_info)


class PrizeHandler(SevenBaseHandler):
    """
    @description: 奖品保存（业务各自实现）
    """
    @filter_check_params("machine_id,prize_name")
    def post_async(self):
        """
        @description: 奖品保存（业务各自实现）
        @param prize_id：奖品id
        @return: 
        @last_editors: HuangJingCan
        """
        pass


class PrizeDelHandler(SevenBaseHandler):
    """
    @description: 删除奖品
    """
    @filter_check_params("prize_id")
    def get_async(self):
        """
        @description: 删除奖品
        @param prize_id：奖品id
        @return: reponse_json_success
        @last_editors: HuangJingCan
        """
        prize_id = int(self.get_param("prize_id", 0))

        if prize_id <= 0:
            return self.reponse_json_error_params()

        ActPrizeModel().del_entity("id=%s", prize_id)

        self.create_operation_log(OperationType.delete.value, "act_prize_tb", "PrizeDelHandler", None, prize_id)

        self.reponse_json_success()


class PrizeDelByThrowHandler(SevenBaseHandler):
    """
    @description: 删除奖品
    """
    @filter_check_params("prize_id")
    def get_async(self):
        """
        @description: 删除奖品
        @param prize_id：奖品id
        @return: reponse_json_success
        @last_editors: HuangJingCan
        """
        prize_id = int(self.get_param("prize_id", 0))

        if prize_id <= 0:
            return self.reponse_json_error_params()

        act_prize_model = ActPrizeModel()
        act_prize = act_prize_model.get_entity("id=%s", params=prize_id)

        if not act_prize:
            return self.reponse_json_success()

        act_prize_model.del_entity("id=%s", prize_id)

        #投放商品处理
        ThrowModel().throw_goods_update(act_prize.act_id, act_prize.goods_id, self.get_now_datetime())

        self.create_operation_log(OperationType.delete.value, "act_prize_tb", "PrizeDelByThrowHandler", None, prize_id)

        self.reponse_json_success()


class PrizeReleaseHandler(SevenBaseHandler):
    """
    @description: 上下架奖品
    """
    @filter_check_params("prize_id")
    def get_async(self):
        """
        @description: 上下架奖品
        @param prize_id：奖品id
        @param is_release：0-下架，1-上架
        @return: 
        @last_editors: HuangJingCan
        """
        prize_id = int(self.get_param("prize_id", 0))
        is_release = int(self.get_param("is_release", 0))
        modify_date = self.get_now_datetime()

        if prize_id <= 0:
            return self.reponse_json_error_params()

        ActPrizeModel().update_table("is_release=%s,modify_date=%s", "id=%s", [is_release, modify_date, prize_id])

        self.reponse_json_success()


class CheckRightEnameHandler(SevenBaseHandler):
    """
    @description: 判断奖品里面有没有添加这张优惠券
    """
    @filter_check_params("right_ename")
    def get_async(self):
        """
        @description: 判断奖品里面有没有添加这张优惠券
        @param right_ename：优惠券标识
        @return reponse_json_success
        @last_editors: HuangJingCan
        """
        right_ename = self.get_param("right_ename")

        count = ActPrizeModel().get_total("right_ename=%s", params=right_ename)
        if count > 0:
            return self.reponse_json_error()

        self.reponse_json_success()