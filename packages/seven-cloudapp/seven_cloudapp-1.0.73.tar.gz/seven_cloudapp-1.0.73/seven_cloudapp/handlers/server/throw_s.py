# -*- coding: utf-8 -*-
"""
@Author: 投放相关
@Date: 2020-06-01 14:07:23
@LastEditTime: 2020-11-24 17:24:21
@LastEditors: HuangJingCan
@Description: 投放相关
"""
from seven_cloudapp.handlers.top_base import *

from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.throw.throw_goods_model import *
from seven_cloudapp.models.db_models.machine.machine_info_model import *
from seven_cloudapp.models.db_models.act.act_prize_model import *
from seven_cloudapp.models.seven_model import *

from seven_cloudapp.libs.customize.seven import *


class InitThrowGoodsListHandler(SevenBaseHandler):
    """
    @description: 初始化活动投放
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 初始化活动投放
        @param app_id：app_id
        @param act_id：活动id
        @return {*}
        @last_editors: CaiYouBin
        """
        app_id = self.get_param("app_id")
        act_id = int(self.get_param("act_id", 0))

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s", params=act_id)

        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，活动不存在")

        machine_info_model = MachineInfoModel()
        act_prize_model = ActPrizeModel()

        machine_goods_id_list = machine_info_model.get_dict_list("act_id=%s and goods_id !=''", field="goods_id", params=act_id)
        prize_goods_id_list = act_prize_model.get_dict_list("act_id=%s and goods_id !='' and goods_id <> 0 ", field="goods_id", params=act_id)

        goods_id_list = []
        if len(machine_goods_id_list) > 0:
            goods_id_list += [int(goods_id["goods_id"]) for goods_id in machine_goods_id_list]
        if len(prize_goods_id_list) > 0:
            goods_id_list += [goods_id["goods_id"] for goods_id in prize_goods_id_list]

        goods_id_list = list(set(goods_id_list))

        if len(goods_id_list) == 0:
            result_data = {"url": f"https://m.duanqu.com/?_ariver_appid={app_id}&query=" + CodingHelper.url_encode(f"actid={act_id}"), "act_name": act_info.act_name, "goods_list": []}
            return self.reponse_json_success(result_data)

        throw_goods_model = ThrowGoodsModel()

        goods_ids = ",".join([str(i) for i in goods_id_list])

        self.logger_info.info("【商品ID】:" + goods_ids)

        throw_goods_exist_list = throw_goods_model.get_dict_list("act_id<>%s and goods_id in (" + goods_ids + ")", field="goods_id", params=act_id)
        throw_goods_id_exist_list = [i for i in throw_goods_exist_list]

        throw_goods_list = []

        for goods_id in goods_id_list:
            throw_goods = ThrowGoods()
            throw_goods.app_id = app_id
            throw_goods.act_id = act_id
            throw_goods.goods_id = goods_id
            if goods_id in throw_goods_id_exist_list:
                throw_goods.is_throw = 0
                throw_goods.is_sync = 0
            else:
                throw_goods.is_throw = 1
                throw_goods.is_sync = 1
            throw_goods.create_date = self.get_now_datetime()
            throw_goods.throw_date = self.get_now_datetime()
            throw_goods.sync_date = self.get_now_datetime()
            throw_goods_list.append(throw_goods)

        throw_goods_model.add_list(throw_goods_list)

        result_data = {"url": f"https://m.duanqu.com/?_ariver_appid={app_id}&query=" + CodingHelper.url_encode(f"actid={act_id}"), "act_name": act_info.act_name, "goods_list": goods_id_list}

        self.reponse_json_success(result_data)


class InitThrowGoodsCallBackHandler(SevenBaseHandler):
    """
    @description: 初始化投放商品回调接口
    """
    def get_async(self):
        """
        @description: 初始化投放商品回调接口
        @param act_id：活动id
        @param close_goods_id：close_goods_id
        @return 
        @last_editors: CaiYouBin
        """
        act_id = int(self.get_param("act_id", "0"))
        close_goods_id = self.get_param("close_goods_id")

        ActInfoModel().update_table("is_throw=1", "id=%s", params=act_id)

        if close_goods_id != "":
            ThrowGoodsModel().update_table("is_throw=0", "act_id=%s and goods_id in (" + close_goods_id + ")", params=act_id)

        self.reponse_json_success()


class SaveThrowGoodsStatusHandler(SevenBaseHandler):
    """
    @description: 保存更改投放商品的状态
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 保存更改投放商品的状态
        @param act_id：活动id
        @param update_goods_id：update_goods_id
        @return 
        @last_editors: CaiYouBin
        """
        act_id = int(self.get_param("act_id", 0))
        update_goods_id = int(self.get_param("update_goods_id", 0))

        if update_goods_id > 0:
            ThrowGoodsModel().update_table("is_throw=abs(is_throw-1),is_sync=0,throw_date=%s", "act_id=%s and goods_id=%s", [self.get_now_datetime(), act_id, update_goods_id])

        self.reponse_json_success()


class ThrowGoodsListHandler(TopBaseHandler):
    """
    @description: 投放商品列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 投放商品列表
        @param act_id：活动id
        @param page_index：页索引
        @param page_size：页大小
        @return 列表
        @last_editors: CaiYouBin
        """
        act_id = int(self.get_param("act_id", 0))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 10))

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s", params=act_id)
        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，活动不存在")

        throw_goods_model = ThrowGoodsModel()
        throw_goods_list, total = throw_goods_model.get_dict_page_list("*", page_index, page_size, "act_id=%s", "", "id desc", params=act_id)

        #获取商品信息
        goods_list = []
        if len(throw_goods_list) > 0:
            goods_ids = ",".join([str(throw_goods["goods_id"]) for throw_goods in throw_goods_list])
            resq = self.get_goods_list_for_goodsids(goods_ids, self.get_taobao_param().access_token)

            if "items_seller_list_get_response" in resq.keys():
                if "item" in resq["items_seller_list_get_response"]["items"].keys():
                    goods_list = resq["items_seller_list_get_response"]["items"]["item"]
            else:
                return self.reponse_json_error(resq["error_code"], resq["error_message"])
        else:
            resq = self.get_goods_list_for_goodsids("", self.get_taobao_param().access_token)

            if "items_seller_list_get_response" in resq.keys():
                if "item" in resq["items_seller_list_get_response"]["items"].keys():
                    goods_list = resq["items_seller_list_get_response"]["items"]["item"]
            else:
                return self.reponse_json_error(resq["error_code"], resq["error_message"])

        throw_goods_list = SevenHelper.merge_dict_list(throw_goods_list, "goods_id", goods_list, "num_iid", "pic_url,title")

        page_info = PageInfo(page_index, page_size, total, throw_goods_list)
        result_data = {"is_throw": act_info.is_throw, "page_info": page_info.__dict__}

        self.reponse_json_success(result_data)


class AsyncThrowGoodsHandler(TopBaseHandler):
    """
    @description: 同步投放商品列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 同步投放商品列表
        @param act_id：活动id
        @return 
        @last_editors: CaiYouBin
        """
        act_id = int(self.get_param("act_id", "0"))

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s", params=act_id)
        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，活动不存在")

        url = f"https://m.duanqu.com/?_ariver_appid={act_info.app_id}&query=" + CodingHelper.url_encode(f"actid={act_info.id}")

        throw_goods_model = ThrowGoodsModel()
        throw_goods_list = throw_goods_model.get_list("act_id=%s and is_sync=0 and is_throw=1", params=act_id)
        no_throw_goods_list = throw_goods_model.get_list("act_id=%s and is_sync=0 and is_throw=0", params=act_id)
        # 同步不投放的商品
        if len(no_throw_goods_list) > 0:

            no_throw_goods_id_list = [str(no_throw_goods.goods_id) for no_throw_goods in no_throw_goods_list]
            no_throw_goods_id_list = list(set(no_throw_goods_id_list))
            no_throw_goods_ids = ",".join(no_throw_goods_id_list)

            update_no_throw_goods_list = []
            # 淘宝top接口
            # resp = self.test_async()
            resp = self.change_throw_goods_list_status(no_throw_goods_ids, url, 'false')
            if "error_response" in resp.keys():
                return self.reponse_json_error("Error", resp["error_response"]["sub_msg"])

            async_result = resp["miniapp_distribution_items_bind_response"]["model_list"]["distribution_order_bind_target_entity_open_result_dto"][0]["bind_result_list"]["distribution_order_bind_base_dto"]
            for async_result_info in async_result:
                no_throw_goods = [no_throw_goods for no_throw_goods in no_throw_goods_list if str(no_throw_goods.goods_id) == async_result_info["target_entity_id"]]
                if len(no_throw_goods) > 0:
                    if async_result_info["success"] == True:
                        no_throw_goods[0].is_sync = 1
                        no_throw_goods[0].sync_date = self.get_now_datetime()
                    else:
                        no_throw_goods[0].error_message = async_result_info["fail_msg"]
                    update_no_throw_goods_list.append(no_throw_goods[0])

            throw_goods_model.update_list(update_no_throw_goods_list)

            self.logger_info.info(str(resp))

        # 同步投放的商品
        if len(throw_goods_list) > 0:
            throw_goods_id_list = [str(throw_goods.goods_id) for throw_goods in throw_goods_list]
            throw_goods_id_list = list(set(throw_goods_id_list))
            throw_goods_ids = ",".join(throw_goods_id_list)

            update_throw_goods_list = []
            # 淘宝top接口
            # resp = self.test_async()
            resp = self.change_throw_goods_list_status(throw_goods_ids, url, 'true')
            if "error_response" in resp.keys():
                return self.reponse_json_error("Error", resp["error_response"]["sub_msg"])

            async_result = resp["miniapp_distribution_items_bind_response"]["model_list"]["distribution_order_bind_target_entity_open_result_dto"][0]["bind_result_list"]["distribution_order_bind_base_dto"]
            for async_result_info in async_result:
                throw_goods = [throw_goods for throw_goods in throw_goods_list if str(throw_goods.goods_id) == async_result_info["target_entity_id"]]
                if len(throw_goods) > 0:
                    if async_result_info["success"] == True:
                        throw_goods[0].is_sync = 1
                        throw_goods[0].sync_date = self.get_now_datetime()
                    else:
                        throw_goods[0].is_throw = 0
                        throw_goods[0].is_sync = 1
                        throw_goods[0].error_message = async_result_info["fail_msg"]
                    update_throw_goods_list.append(throw_goods[0])

            throw_goods_model.update_list(update_throw_goods_list)

            self.logger_info.info(str(resp))

        self.reponse_json_success()

    def test_async(self):
        result = {
            'miniapp_distribution_items_bind_response': {
                'model_list': {
                    'distribution_order_bind_target_entity_open_result_dto': [{
                        'bind_result_list': {
                            'distribution_order_bind_base_dto': [{
                                'fail_msg': '商品不存在',
                                'success': False,
                                'target_entity_id': '55'
                            }, {
                                'fail_msg': '商品不存在',
                                'success': False,
                                'target_entity_id': '2'
                            }, {
                                'fail_msg': '2020 : 实体绑定关系不存在',
                                'success': False,
                                'target_entity_id': '613878861009'
                            }, {
                                'fail_msg': '2020 : 实体绑定关系不存在',
                                'success': False,
                                'target_entity_id': '620482163358'
                            }, {
                                'fail_msg': '商品不属于当前商家',
                                'success': False,
                                'target_entity_id': '620003498461'
                            }, {
                                'success': True,
                                'target_entity_id': '620480991439'
                            }, {
                                'success': True,
                                'target_entity_id': '616454842353'
                            }, {
                                'fail_msg': '商品不属于当前商家',
                                'success': False,
                                'target_entity_id': '573998736785'
                            }, {
                                'fail_msg': '2020 : 实体绑定关系不存在',
                                'success': False,
                                'target_entity_id': '619094193197'
                            }, {
                                'fail_msg': '商品不存在',
                                'success': False,
                                'target_entity_id': '10'
                            }]
                        },
                        'scene_name': '详情悬浮',
                        'url': 'https://m.duanqu.com/?_ariver_appid=3000000006168005&query=actid%3D133'
                    }]
                },
                'request_id': '4kc53bm4dfjg'
            }
        }
        return result