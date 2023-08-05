# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-08-12 09:06:24
@LastEditTime: 2020-11-26 14:25:02
@LastEditors: HuangJingCan
@Description: 淘宝top接口基础类
"""
from seven_cloudapp.handlers.seven_base import *

from seven_top import top

from seven_cloudapp.models.enum import *

from seven_cloudapp.models.db_models.act.act_prize_model import *
from seven_cloudapp.models.db_models.base.base_info_model import *
from seven_cloudapp.models.db_models.app.app_info_model import *


class TopBaseHandler(SevenBaseHandler):
    """
    @description: 淘宝top接口基础类
    """
    def get_sku_info(self, num_iids, access_token):
        """
        @description: 获取sku信息
        @param num_iids：num_iids
        @param access_token：access_token
        @return 
        @last_editors: HuangJingCan
        """
        if self.get_is_test() == True:
            sku_info = self.test_sku_info()
            return self.reponse_json_success(sku_info)

        resp = self.get_goods_list_for_goodsids(num_iids, access_token)

        # self.logger_info.info(str(resp) + "【access_token】：" + self.get_taobao_param().access_token)
        if "items_seller_list_get_response" in resp.keys():
            if "items" in resp["items_seller_list_get_response"].keys():
                self.reponse_json_success(resp["items_seller_list_get_response"])
            else:
                prize = ActPrizeModel().get_entity("goods_id=%s and sku_detail<>'' and is_sku=1 ", params=int(num_iids))
                if prize:
                    sku_detail = json.loads(prize.sku_detail.replace('\'', '\"'))
                    self.reponse_json_success(sku_detail["items_seller_list_get_response"])
                else:
                    self.reponse_json_error("NoSku", "对不起，找不到该商品的sku")
        else:
            self.reponse_json_success(resp)

    def get_sku_name(self, num_iids, sku_id, access_token):
        """
        @description: 获取sku名称
        @param num_iids：num_iids
        @param sku_id：sku_id
        @param access_token：access_token
        @return 
        @last_editors: HuangJingCan
        """
        if self.get_is_test() == True:
            return self.reponse_json_success(self.test_sku_info())

        top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
        req = top.api.ItemsSellerListGetRequest()

        req.fields = "num_iid,title,nick,input_str,property_alias,sku,props_name,pic_url"
        req.num_iids = num_iids

        resp = req.getResponse(access_token)

        # self.logger_info.info(str(resp) + "【access_token】：" + self.get_taobao_param().access_token)
        if "items_seller_list_get_response" in resp.keys():
            if "items" in resp["items_seller_list_get_response"].keys():
                props_names = resp["items_seller_list_get_response"]["items"]["item"][0]["props_name"].split(';')
                for sku in resp["items_seller_list_get_response"]["items"]["item"][0]["skus"]["sku"]:
                    if sku["sku_id"] == sku_id:
                        props_name = [i for i in props_names if sku["properties"] in i]
                        if len(props_name) > 0:
                            # self.logger_info.info(props_name[0][(len(sku["properties"]) + 1):])
                            return props_name[0][(len(sku["properties"]) + 1):]
                        else:
                            # self.logger_info.info(sku["properties_name"].split(':')[1])
                            return sku["properties_name"].split(':')[1]
        return ""

    def test_sku_info(self):
        sku_info = {
            "items": {
                "item": [{
                    "input_str": "984055037,棉95% 聚氨酯弹性纤维(氨纶)5%,粉色-女款;颜色分类;黄色-男款",
                    "nick": "阪织屋旗舰店",
                    "num_iid": 615956945446,
                    "pic_url": "https://img.alicdn.com/bao/uploaded/i3/2089529736/O1CN01GdsGYs2Ln8i0Dxv3c_!!0-item_pic.jpg",
                    "property_alias": "",
                    "props_name":
                    "20000:223946830:品牌:阪织屋;20021:105255:面料主材质:棉;20509:28314:尺码:S;20509:28315:尺码:M;20509:28316:尺码:L;20509:28317:尺码:XL;20603:14031880:图案:卡通动漫;20608:31755:家居服风格:卡通;24477:47698:适用性别:情侣;31745:3500872:件数:2件;1627207:380784160:颜色分类:粉色-女款;1627207:15039988:颜色分类:黄色-男款;8560225:828918270:上市时间:2020年夏季;13021751:7837058106:款号:984055037;13328588:493262620:成分含量:81%(含)-95%(含);122216507:3216783:厚薄:薄款;122216515:4060838:适用场景:休闲家居;122216608:3267959:适用对象:青年;148380063:852538341:销售渠道类型:纯电商(只在线上销售);149422948:854658283:面料材质成分:棉95% 聚氨酯弹性纤维(氨纶)5%",
                    "skus": {
                        "sku": [{
                            "created": "2020-04-14 16:21:58",
                            "modified": "2020-06-21 00:07:43",
                            "outer_id": "9840550372101",
                            "price": "329.00",
                            "properties": "1627207:380784160;20509:28314",
                            "properties_name": "1627207:380784160:颜色分类:粉色-女款;20509:28314:尺码:S",
                            "quantity": 28,
                            "sku_id": 4511701590232
                        }, {
                            "created": "2020-04-14 16:21:58",
                            "modified": "2020-06-21 00:07:43",
                            "outer_id": "9840550372102",
                            "price": "329.00",
                            "properties": "1627207:380784160;20509:28315",
                            "properties_name": "1627207:380784160:颜色分类:粉色-女款;20509:28315:尺码:M",
                            "quantity": 73,
                            "sku_id": 4511701590233
                        }, {
                            "created": "2020-04-14 16:21:58",
                            "modified": "2020-06-21 00:07:43",
                            "outer_id": "9840550372103",
                            "price": "329.00",
                            "properties": "1627207:380784160;20509:28316",
                            "properties_name": "1627207:380784160:颜色分类:粉色-女款;20509:28316:尺码:L",
                            "quantity": 71,
                            "sku_id": 4511701590234
                        }, {
                            "created": "2020-04-14 16:21:58",
                            "modified": "2020-06-21 00:07:43",
                            "outer_id": "9840550384002",
                            "price": "369.00",
                            "properties": "1627207:15039988;20509:28315",
                            "properties_name": "1627207:15039988:颜色分类:黄色-男款;20509:28315:尺码:M",
                            "quantity": 0,
                            "sku_id": 4511701590235
                        }, {
                            "created": "2020-04-14 16:21:58",
                            "modified": "2020-06-21 00:07:43",
                            "outer_id": "9840550384003",
                            "price": "369.00",
                            "properties": "1627207:15039988;20509:28316",
                            "properties_name": "1627207:15039988:颜色分类:黄色-男款;20509:28316:尺码:L",
                            "quantity": 53,
                            "sku_id": 4511701590236
                        }, {
                            "created": "2020-04-14 16:21:58",
                            "modified": "2020-06-21 00:07:43",
                            "outer_id": "9840550384004",
                            "price": "369.00",
                            "properties": "1627207:15039988;20509:28317",
                            "properties_name": "1627207:15039988:颜色分类:黄色-男款;20509:28317:尺码:XL",
                            "quantity": 23,
                            "sku_id": 4511701590237
                        }]
                    },
                    "title": "阪织屋睡衣女迪士尼情侣睡衣米老鼠棉质印花女士短袖短裤套头套装"
                }]
            }
        }
        return sku_info

    def get_taobao_order(self, open_id, access_token, start_created="", end_created=""):
        """
        @description: 获取淘宝订单
        @param open_id：open_id
        @param access_token：access_token
        @param start_created：开始时间
        @param end_created：结束时间
        @return 
        @last_editors: HuangJingCan
        """
        all_order = []
        has_next = True

        top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
        req = top.api.OpenTradesSoldGetRequest()

        req.fields = "tid,status,payment,price,created,orders,num,pay_time"
        req.type = "fixed"
        req.buyer_open_id = open_id
        req.page_size = 10
        req.page_no = 1
        req.use_has_next = "true"

        if start_created == "":
            start_timestamp = TimeHelper.get_now_timestamp() - 90 * 24 * 60 * 60
            start_created = TimeHelper.timestamp_to_format_time(start_timestamp)
        # start_created = "2020-06-01 00:00:00"
        req.start_created = start_created
        if end_created != "":
            req.end_created = end_created

        while has_next:
            resp = req.getResponse(access_token)

            # self.logger_info.info(str(resp) + "【access_token】：" + self.get_taobao_param().access_token + "【获取订单】")
            if "open_trades_sold_get_response" in resp.keys():
                if "trades" in resp["open_trades_sold_get_response"].keys():
                    all_order = all_order + resp["open_trades_sold_get_response"]["trades"]["trade"]
                req.page_no += 1
                has_next = resp["open_trades_sold_get_response"]["has_next"]

        return all_order

    def test_order(self):
        test_order = '''
            [
                {
                "created": "2020-06-13 19:10:39",
                "price": "1.00",
                "num": 1,
                "payment": "1.00",
                "orders": {
                    "order": [
                    {
                        "refund_status": "Success",
                        "price": "1.00",
                        "num": 1,
                        "payment": "1.00",
                        "num_iid": 573998736785,
                        "pic_path": "https://img.alicdn.com/bao/uploaded/i2/2960093539/O1CN01onsXQ61c0uFhJBqiu_!!0-item_pic.jpg",
                        "sku_id": "4299761829877",
                        "oid": "820019170235115377",
                        "title": "歪瓜出品 测试链接请勿拍下 拍下不发货",
                        "status": "WAIT_SELLER_SEND_GOODS"
                    }
                    ]
                },
                "tid": "819703136929115378",
                "pay_time": "2020-06-13 19:10:44",
                "status": "WAIT_SELLER_SEND_GOODS"
                },
                {
                "created": "2020-05-09 17:09:49",
                "price": "1.00",
                "num": 1,
                "payment": "1.00",
                "orders": {
                    "order": [
                    {
                        "refund_status": "NO_REFUND",
                        "price": "1.00",
                        "num": 1,
                        "payment": "1.00",
                        "num_iid": 573998736786,
                        "pic_path": "https://img.alicdn.com/bao/uploaded/i2/2960093539/O1CN01onsXQ61c0uFhJBqiu_!!0-item_pic.jpg",
                        "sku_id": "4299761829877",
                        "oid": "820019170235115377",
                        "title": "歪瓜出品 测试链接请勿拍下 拍下不发货",
                        "status": "TRADE_CLOSED_BY_TAOBAO"
                    }
                    ]
                },
                "tid": "820019170235115377",
                "status": "TRADE_CLOSED_BY_TAOBAO"
                },
                {
                "created": "2020-05-09 17:09:09",
                "price": "1.00",
                "num": 1,
                "payment": "1.00",
                "orders": {
                    "order": [
                    {
                        "refund_status": "NO_REFUND",
                        "price": "1.00",
                        "num": 1,
                        "payment": "1.00",
                        "num_iid": 573998736786,
                        "pic_path": "https://img.alicdn.com/bao/uploaded/i2/2960093539/O1CN01onsXQ61c0uFhJBqiu_!!0-item_pic.jpg",
                        "sku_id": "4299761829877",
                        "oid": "820019362005115377",
                        "title": "歪瓜出品 测试链接请勿拍下 拍下不发货",
                        "status": "WAIT_BUYER_PAY"
                    }
                    ]
                },
                "tid": "820019362005115377",
                "status": "WAIT_BUYER_PAY"
                }
            ]
            '''
        return test_order

    def rewards_status(self):
        """
        @description: rewards_status
        @param 
        @return: 
        @last_editors: CaiYouBin
        """
        status = [
            #等待卖家发货
            "WAIT_SELLER_SEND_GOODS",
            #卖家部分发货
            "SELLER_CONSIGNED_PART",
            #等待买家确认收货
            "WAIT_BUYER_CONFIRM_GOODS",
            #买家已签收（货到付款专用）
            "TRADE_BUYER_SIGNED",
            #交易成功
            "TRADE_FINISHED"
        ]
        return status

    def refund_status(self):
        """
        @description: 给予奖励的子订单退款状态
        @param 
        @return: 
        @last_editors: CaiYouBin
        """
        status = [
            #没有退款
            "NO_REFUND",
            #退款关闭
            "CLOSED",
            #卖家拒绝退款
            "WAIT_SELLER_AGREE"
        ]
        return status

    def instantiate(self, user_nick, act_name, description, icon, name_ending):
        """
        @description: 实例化
        @param user_nick：用户昵称
        @param act_name：活动名称
        @param description：活动简介
        @param icon：活动图标
        @param name_ending：名称结尾
        @return app_info
        @last_editors: HuangJingCan
        """
        open_id = self.get_taobao_param().open_id

        app_info_model = AppInfoModel()
        store_user_nick = user_nick.split(':')[0]
        app_info = app_info_model.get_entity("store_user_nick=%s", params=store_user_nick)
        if not app_info:
            if ":" in user_nick:
                return self.reponse_json_error("Error", "对不起，初次创建活动包含实例化，请试用主账号进行创建。")
            base_info_model = BaseInfoModel()
            base_info = base_info_model.get_entity()
            template_id = config.get_value("client_template_id")
            template_version = base_info.client_ver
            access_token = self.get_taobao_param().access_token
            app_info = self.instantiate_app(user_nick, open_id, description, icon, act_name, template_id, template_version, 1, access_token, name_ending)

            if isinstance(app_info, dict):
                if "error" in app_info.keys():
                    return self.reponse_json_error(app_info["error"], app_info["message"])

            self.create_operation_log(OperationType.add.value, app_info.__str__(), "instantiate", None, self.json_dumps(app_info))

        return app_info

    def instantiate_app(self, user_nick, open_id, description, icon, name, template_id, template_version, isfirst, access_token, name_ending):
        """
        @description: 实例化
        @param user_nick：用户昵称
        @param open_id：用户唯一标识
        @param description：活动简介
        @param icon：活动图标
        @param name：活动名称
        @param template_id：模板id
        @param template_version：模板版本
        @param isfirst：是否第一次
        @param access_token：access_token
        @param name_ending：name_ending
        @return app_info
        @last_editors: HuangJingCan
        """
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.MiniappTemplateInstantiateRequest()

            req.clients = "taobao,tmall"
            req.description = description
            shop_info = self.get_shop(access_token)

            if isfirst == 1:
                app_name = shop_info["shop_seller_get_response"]["shop"]["title"] + name_ending
            else:
                app_name = name
            # self.logger_info.info("【实例化名称】" + ":" + str(app_name))
            req.ext_json = "{ \"name\":\"" + app_name + "\"}"
            req.icon = icon
            req.name = app_name
            req.template_id = template_id
            req.template_version = template_version
            resp = req.getResponse(access_token)

            #录入数据库
            result_app = resp["miniapp_template_instantiate_response"]
            app_info_model = AppInfoModel()
            app_info = AppInfo()
            app_info.clients = req.clients
            app_info.app_desc = result_app["app_description"]
            app_info.app_icon = result_app["app_icon"]
            app_info.app_id = result_app["app_id"]
            app_info.app_name = result_app["app_name"]
            app_info.app_ver = result_app["app_version"]
            app_info.app_key = result_app["appkey"]
            app_info.preview_url = result_app["pre_view_url"]
            app_info.template_id = req.template_id
            app_info.template_ver = req.template_version

            if "shop_seller_get_response" in shop_info.keys():
                app_info.store_name = shop_info["shop_seller_get_response"]["shop"]["title"]
                app_info.store_id = shop_info["shop_seller_get_response"]["shop"]["sid"]

            user_seller = self.get_user_seller(access_token)
            if "user_seller_get_response" in user_seller.keys():
                app_info.seller_id = user_seller["user_seller_get_response"]["user"]["user_id"]

            app_info.is_instance = 1
            app_info.store_user_nick = user_nick.split(':')[0]
            app_info.owner_open_id = open_id
            app_info.instance_date = self.get_now_datetime()
            app_info.modify_date = self.get_now_datetime()
            #上线
            online_app_info = self.online_app(app_info.app_id, template_id, template_version, app_info.app_ver, access_token)
            if "miniapp_template_onlineapp_response" in online_app_info.keys():
                app_info.app_url = online_app_info["miniapp_template_onlineapp_response"]["app_info"]["online_url"]

            app_info.id = AppInfoModel().add_entity(app_info)

            return app_info
        except Exception as ex:
            self.logger_error.error(str(ex))
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=" in content:
                        if "名称已经存在" in content:
                            if isfirst == 1:
                                return self.instantiate_app(user_nick, open_id, description, icon, name, template_id, template_version, 0, access_token, name_ending)
                            else:
                                return {"error": "CreateError", "message": content[len("submsg="):]}
                        if "应用名称不合法" in content:
                            if isfirst == 1:
                                return self.instantiate_app(user_nick, open_id, description, icon, name, template_id, template_version, 0, access_token, name_ending)
                            else:
                                return {"error": "CreateError", "message": content[len("submsg="):]}
                        return {"error": "CreateError", "message": content[len("submsg="):]}

    def online_app(self, app_id, template_id, template_version, app_version, access_token):
        """
        @description: app上线
        @param app_id：app_id
        @param template_id：模板id
        @param template_version：模板版本
        @param app_version：app版本
        @param access_token：access_token
        @return 
        @last_editors: HuangJingCan
        """
        top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
        req = top.api.MiniappTemplateOnlineappRequest()

        req.clients = "taobao,tmall"
        req.app_id = app_id
        req.template_id = template_id
        req.template_version = template_version
        req.app_version = app_version
        resp = req.getResponse(access_token)
        return resp

    def get_shop(self, access_token):
        """
        @description: 获取店铺信息
        @param access_token：access_token
        @return: 
        @last_editors: HuangJingCan
        """
        top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
        req = top.api.ShopSellerGetRequest()

        req.fields = "sid,title,pic_path"
        resp = req.getResponse(access_token)
        return resp

    def get_user_seller(self, access_token):
        """
        @description: 获取关注店铺用户信息
        @param access_token：access_token
        @return: 
        @last_editors: HuangJingCan
        """
        top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
        req = top.api.UserSellerGetRequest()

        req.fields = "user_id,nick,sex"
        resp = req.getResponse(access_token)
        return resp

    def get_dead_date(self, user_nick):
        """
        @description: 获取过期时间
        @param user_nick：用户昵称
        @return 
        @last_editors: HuangJingCan
        """
        if self.get_is_test() == True:
            return config.get_value("test_dead_date")
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.VasSubscribeGetRequest()

            req.article_code = config.get_value("article_code")
            req.nick = user_nick
            resp = req.getResponse(self.get_taobao_param().access_token)
            if "article_user_subscribe" not in resp["vas_subscribe_get_response"]["article_user_subscribes"].keys():
                return "expire"
            else:
                return resp["vas_subscribe_get_response"]["article_user_subscribes"]["article_user_subscribe"][0]["deadline"]
        except Exception as ex:
            self.logger_info.info("get_dead_date:" + str(ex))
            return config.get_value("test_dead_date")

    def get_token(self):
        """
        @description: 获取授权token
        @param 
        @return: 
        @last_editors: CaiYouBin
        """
        if self.get_is_test() == True:
            return ""

        top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
        req = top.api.ItemsOnsaleGetRequest()

        req.fields = "num_iid,title,nick,input_str,property_alias,sku,props_name,pic_url"
        req.page_no = 1
        req.page_size = 10

        try:
            resp = req.getResponse(self.get_taobao_param().access_token)

            return self.get_taobao_param().access_token
        except Exception as ex:
            return ""

    def get_goods_list(self, page_index, page_size, goods_name, order_tag, order_by, access_token):
        """
        @description: 导入商品列表（获取当前会话用户出售中的商品列表）
        @param page_index：页索引
        @param page_size：页大小
        @param goods_name：商品名称
        @param order_tag：order_tag
        @param order_by：排序类型
        @param access_token：access_token
        @return 
        @last_editors: HuangJingCan
        """
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.ItemsOnsaleGetRequest()

            req.fields = "num_iid,title,nick,price,input_str,property_alias,sku,props_name,pic_url"
            req.page_no = page_index + 1
            req.page_size = page_size
            if goods_name != "":
                req.q = goods_name
            req.order_by = order_tag + ":" + order_by

            resp = req.getResponse(access_token)
            if resp:
                resp["pageSize"] = page_size
                resp["pageIndex"] = page_index

            # self.logger_info.info(str(resp) + "【access_token】：" + self.get_taobao_param().access_token)
            self.reponse_json_success(resp)
        except Exception as ex:
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return self.reponse_json_error("NoPower", content[len("submsg="):])
                    if "submsg=" in content:
                        return self.reponse_json_error("Error", content[len("submsg="):])

    def test_goods_list(self):
        """
        @description: 测试商品列表
        @param {type} 
        @return {type} 
        @last_editors: HuangJingCan
        """
        goods_list_json = {
            'items_onsale_get_response': {
                'items': {
                    'item': [{
                        'nick': 'loveyouhk',
                        'num_iid': 619094193197,
                        'pic_url': 'https://img.alicdn.com/bao/uploaded/i2/305104024/T2YY4jXfXcXXXXXXXX_!!305104024.jpg',
                        'title': '测试5'
                    }, {
                        'nick': 'loveyouhk',
                        'num_iid': 619618211537,
                        'pic_url': 'https://img.alicdn.com/bao/uploaded/i4/305104024/O1CN01H7Leza1fb2MFvH3V9_!!305104024.jpg',
                        'title': '测试4'
                    }, {
                        'nick': 'loveyouhk',
                        'num_iid': 616454842353,
                        'pic_url': 'https://img.alicdn.com/bao/uploaded/i1/305104024/O1CN0123kpnE1fb2MHUgGsr_!!305104024.jpg',
                        'title': '测试宝贝3'
                    }, {
                        'nick': 'loveyouhk',
                        'num_iid': 620482187181,
                        'pic_url': 'https://img.alicdn.com/bao/uploaded/i2/305104024/T2YY4jXfXcXXXXXXXX_!!305104024.jpg',
                        'title': '测试宝贝9'
                    }, {
                        'nick': 'loveyouhk',
                        'num_iid': 620482163358,
                        'pic_url': 'https://img.alicdn.com/bao/uploaded/i1/305104024/O1CN01XWvOUt1fb2N6fanuW_!!305104024.png',
                        'title': '测试宝贝10测试宝贝10测试宝贝10测试宝贝10测试宝贝10测试宝贝10'
                    }, {
                        'nick': 'loveyouhk',
                        'num_iid': 620215826949,
                        'pic_url': 'https://img.alicdn.com/bao/uploaded/i1/305104024/O1CN01XWvOUt1fb2N6fanuW_!!305104024.png',
                        'title': '测试宝贝8'
                    }, {
                        'nick': 'loveyouhk',
                        'num_iid': 620480991439,
                        'pic_url': 'https://img.alicdn.com/bao/uploaded/i1/305104024/O1CN01XWvOUt1fb2N6fanuW_!!305104024.png',
                        'title': '测试宝贝7'
                    }, {
                        'nick': 'loveyouhk',
                        'num_iid': 616631743105,
                        'pic_url': 'https://img.alicdn.com/bao/uploaded/i1/305104024/O1CN0123kpnE1fb2MHUgGsr_!!305104024.jpg',
                        'title': '测试宝贝2'
                    }, {
                        'nick': 'loveyouhk',
                        'num_iid': 613878861009,
                        'pic_url': 'https://img.alicdn.com/bao/uploaded/i1/305104024/O1CN0123kpnE1fb2MHUgGsr_!!305104024.jpg',
                        'title': '测试商品1'
                    }]
                },
                'total_results': 9,
                'request_id': '3gx6au6cs9y0'
            },
            'pageSize': 10,
            'pageIndex': 0
        }
        return goods_list_json

    def get_goods_list_client(self, page_index, page_size, access_token):
        """
        @description: 导入商品列表（客户端）
        @param page_index：页索引
        @param page_size：页大小
        @param access_token：access_token
        @return 
        @last_editors: HuangJingCan
        """
        try:
            resp = {}
            if self.get_is_test() == True:
                resp = self.test_goods_list()
            else:
                top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
                req = top.api.ItemsOnsaleGetRequest()

                req.fields = "num_iid,title,nick,pic_url,price"
                req.page_no = page_index + 1
                req.page_size = page_size

                resp = req.getResponse(access_token)
                # self.logger_info.info(str(resp))
            goods_list = []
            if "items_onsale_get_response" in resp.keys():
                if "items" in resp["items_onsale_get_response"]:
                    if "item" in resp["items_onsale_get_response"]["items"]:
                        if len(resp["items_onsale_get_response"]["items"]["item"]) > 10:
                            goods_index_list = range(len(resp["items_onsale_get_response"]["items"]["item"]))
                            indexs = random.sample(goods_index_list, 10)
                            for i in range(0, 10):
                                goods_list.append(resp["items_onsale_get_response"]["items"]["item"][indexs[i]])
                        else:
                            goods_list = resp["items_onsale_get_response"]["items"]["item"]

                        random.randint(0, len(resp["items_onsale_get_response"]["items"]["item"]))
            if resp:
                resp["pageSize"] = page_size
                resp["pageIndex"] = page_index

            self.reponse_json_success(goods_list)
        except Exception as ex:
            # self.logger_info.info(str(ex) + "【access_token】：" + self.get_taobao_param().access_token)
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return self.reponse_json_error("NoPower", content[len("submsg="):])
                    if "submsg=" in content:
                        return self.reponse_json_error("Error", content[len("submsg="):])

    def get_goods_info(self, num_iid, access_token):
        """
        @description: 导入商品列表
        @param num_iids：num_iids
        @param access_token：access_token
        @return 
        @last_editors: HuangJingCan
        """
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.ItemSellerGetRequest()

            req.fields = "num_iid,title,nick,pic_url,price,item_img.url,outer_id,sku,approve_status"
            req.num_iid = num_iid

            resp = req.getResponse(access_token)
            # self.logger_info.info(str(resp))
            self.reponse_json_success(resp)
        except Exception as ex:
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return self.reponse_json_error("NoPower", content[len("submsg="):])
                    if "submsg=该商品已被删除" in content:
                        return self.reponse_json_error("GoodsDel", content[len("submsg="):])
                    if "submsg=" in content:
                        return self.reponse_json_error("Error", content[len("submsg="):])

    def test_goods_info(self):
        """
        @description: 测试商品
        @param {type} 
        @return {type} 
        @last_editors: HuangJingCan
        """
        goods_json = {
            'item_seller_get_response': {
                'item': {
                    'props_name': '20000:3275069:品牌:盈讯;1753146:3485013:型号:F908;30606:112030:上市时间:2008年',
                    'property_alias': '20000:3275069:盈讯;1753146:3485013:F908;30606:112030:2008年',
                    'approve_status': 'onsale',
                    'item_imgs': {
                        'item_img': [{
                            'url': 'https://img.alicdn.com/bao/uploaded/i2/2960093539/O1CN01IHRzmN1c0uHV10kHG_!!2960093539-0-lubanu-s.jpg'
                        }, {
                            'url': 'https://img.alicdn.com/bao/uploaded/i4/2960093539/O1CN01vHPntd1c0uHU5Yk9u_!!2960093539-0-lubanu-s.jpg'
                        }, {
                            'url': 'https://img.alicdn.com/bao/uploaded/i1/2960093539/O1CN01VSRPZk1c0uHaEcUUs_!!2960093539-0-lubanu-s.jpg'
                        }, {
                            'url': 'https://img.alicdn.com/bao/uploaded/i3/2960093539/O1CN018piHzr1c0uHTeKlAo_!!2960093539-0-lubanu-s.jpg'
                        }, {
                            'url': 'https://img.alicdn.com/bao/uploaded/i3/2960093539/O1CN01z2Qfot1c0uHZBEds4_!!2960093539-0-lubanu-s.jpg'
                        }]
                    },
                    'nick': '歪瓜出品旗舰店',
                    'num_iid': 620003498461,
                    'pic_url': 'https://img.alicdn.com/bao/uploaded/i2/2960093539/O1CN01IHRzmN1c0uHV10kHG_!!2960093539-0-lubanu-s.jpg',
                    'price': '60.00',
                    'skus': {
                        'sku': [{
                            'created': '2020-06-05 14:53:50',
                            'modified': '2020-06-10 15:29:53',
                            'outer_id': 'XNYY-ND001',
                            'price': '60.00',
                            'properties': '134942334:28316;1627207:3232483',
                            'properties_name': '134942334:28316:大小:L;1627207:3232483:颜色分类:军绿色',
                            'quantity': 1000,
                            'sku_id': 4552779199857
                        }, {
                            'created': '2020-06-05 14:53:50',
                            'modified': '2020-06-10 15:29:53',
                            'outer_id': 'XNYY-ND002',
                            'price': '120.00',
                            'properties': '134942334:28316;1627207:90554',
                            'properties_name': '134942334:28316:大小:L;1627207:90554:颜色分类:桔色',
                            'quantity': 1000,
                            'sku_id': 4552779199858
                        }, {
                            'created': '2020-06-05 14:53:50',
                            'modified': '2020-06-10 15:29:53',
                            'outer_id': 'XNYY-ND003',
                            'price': '200.00',
                            'properties': '134942334:28316;1627207:60092',
                            'properties_name': '134942334:28316:大小:L;1627207:60092:颜色分类:浅黄色',
                            'quantity': 1000,
                            'sku_id': 4552779199859
                        }, {
                            'created': '2020-06-05 14:53:50',
                            'modified': '2020-06-10 15:29:53',
                            'outer_id': 'XNYY-ND004',
                            'price': '600.00',
                            'properties': '134942334:28316;1627207:3232479',
                            'properties_name': '134942334:28316:大小:L;1627207:3232479:颜色分类:深紫色',
                            'quantity': 1000,
                            'sku_id': 4552779199860
                        }, {
                            'created': '2020-06-05 14:53:50',
                            'modified': '2020-06-10 15:29:53',
                            'outer_id': 'XNYY-ND005',
                            'price': '1200.00',
                            'properties': '134942334:28316;1627207:3232480',
                            'properties_name': '134942334:28316:大小:L;1627207:3232480:颜色分类:粉红色',
                            'quantity': 1000,
                            'sku_id': 4552779199861
                        }]
                    },
                    'title': '歪瓜出品 在线抽盒机一番赏扭蛋盲盒 扭蛋币购买不支持退货退款'
                },
                'request_id': '3pwgypud7ycy'
            }
        }
        return goods_json

    def app_update(self):
        """
        @description: app更新
        @param 
        @return 
        @last_editors: HuangJingCan
        """
        app_id = self.get_param("app_id")
        client_template_id = config.get_value("client_template_id")
        test_client_ver = config.get_value("test_client_ver")
        access_token = self.get_taobao_param().access_token

        base_info = BaseInfoModel().get_entity()
        client_ver = base_info.client_ver

        app_info_model = AppInfoModel()
        app_info = app_info_model.get_entity("app_id=%s", params=app_id)
        if not app_info:
            return self.reponse_json_error("NoApp", "对不起，找不到该APP")
        old_app_info = app_info

        #指定账号升级
        if test_client_ver:
            user_nick = self.get_taobao_param().user_nick
            if user_nick:
                if user_nick == config.get_value("test_user_nick"):
                    client_ver = test_client_ver

        #更新
        top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
        req = top.api.MiniappTemplateUpdateappRequest()

        req.clients = "taobao,tmall"
        req.app_id = app_id
        req.template_id = client_template_id
        req.template_version = client_ver
        try:
            resp = req.getResponse(access_token)

            if resp and ("miniapp_template_updateapp_response" in resp.keys()):
                app_version = resp["miniapp_template_updateapp_response"]["app_version"]
                online_app_info = self.online_app(app_id, client_template_id, client_ver, app_version, access_token)
                if "miniapp_template_onlineapp_response" in online_app_info.keys():
                    app_info.app_ver = resp["miniapp_template_updateapp_response"]["app_version"]
                    app_info.template_ver = client_ver
                    app_info.modify_date = self.get_now_datetime()
                    app_info_model.update_entity(app_info)

            # self.logger_info.info(str(resp) + "【更新】")

            self.create_operation_log(OperationType.update.value, app_info.__str__(), "AppUpdateHandler", self.json_dumps(old_app_info), self.json_dumps(app_info))

            self.reponse_json_success()
        except Exception as ex:
            if "submsg" in str(ex):
                self.logger_error.error(str(ex) + "【更新】")
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return self.reponse_json_error("NoPower", content[len("submsg="):])
                    if "submsg=" in content:
                        return self.reponse_json_error("Error", content[len("submsg="):])


    def change_throw_goods_list_status(self, throw_goods_ids, url, status):
        """
        @description: change_throw_goods_list_status
        @param throw_goods_ids：throw_goods_ids
        @param url：链接地址
        @param status：状态
        @return 
        @last_editors: HuangJingCan
        """
        top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
        req = top.api.MiniappDistributionItemsBindRequest()

        req.target_entity_list = throw_goods_ids
        req.url = url
        req.add_bind = status
        resp = req.getResponse(self.get_taobao_param().access_token)
        return resp

    def get_goods_list_for_goodsids(self, num_iids, access_token):
        """
        @description: 批量获取商品详细信息
        @param num_iids：商品id列表
        @param access_token：access_token
        @return list
        @last_editors: HuangJingCan
        """
        try:
            top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
            req = top.api.ItemsSellerListGetRequest()

            req.fields = "num_iid,title,nick,input_str,property_alias,sku,props_name,pic_url"
            req.num_iids = num_iids
            resp = req.getResponse(access_token)
            return resp
        except Exception as ex:
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        return {"error_code": "NoPower", "error_message": content[len("submsg="):]}
                    if "submsg=" in content:
                        return {"error_code": "Error", "error_message": content[len("submsg="):]}

    def get_taobao_order_info(self, order_no, access_token):
        """
        @description: 获取单笔订单
        @param order_no：订单编号
        @param access_token：access_token
        @return: 
        @last_editors: CaiYouBin
        """
        top.setDefaultAppInfo(config.get_value("app_key"), config.get_value("app_secret"))
        req = top.api.OpenTradeGetRequest()

        req.fields = "tid,status,payment,price,created,orders,num,pay_time,buyer_open_uid"
        req.tid = order_no

        resp = req.getResponse(access_token)

        if "open_trade_get_response" in resp.keys():
            if "trade" in resp["open_trade_get_response"]:
                return resp["open_trade_get_response"]["trade"]
            return None

    def test_order_info(self):
        test_order = {
            "open_trade_get_response": {
                "trade": {
                    "tid": "819703136929115378",
                    "num": 1,
                    "num_iid": 3424234,
                    "status": "TRADE_NO_CREATE_PAY",
                    "type": "fixed(一口价)",
                    "price": "5.00",
                    "total_fee": "5.00",
                    "created": "2000-01-01 00:00:00",
                    "orders": {
                        "order": [{
                            "outer_iid": "152e442aefe88dd41cb0879232c0dcb0",
                            "oid": "819703136929115378",
                            "status": "TRADE_NO_CREATE_PAY",
                            "price": "5.00",
                            "num_iid": 2342344,
                            "sku_id": "5937146",
                            "num": 1,
                            "outer_sku_id": "81893848",
                            "total_fee": "5.00",
                            "pic_path": "http:\/\/img08.taobao.net\/bao\/uploaded\/i8\/T1jVXXXePbXXaoPB6a_091917.jpg",
                            "title": "测试机器",
                            "payment": "5.00",
                            "customization": "{ \"itemId\": 123, \"skuId\": 123, \"text\": [ { \"id\": 44, \"content\": \"home\" } ], \"pic\": [ { \"id\": 44, \"url\": \"sn\" } ] ,\"dingzhi\":\";pluginId:182;dingzhiId:157886;\"}"
                        }]
                    },
                    "payment": "5.00",
                    "buyer_open_uid": "AAFisaLrAKYmeFNoo7oWNA5S",
                    "pay_time": "2000-01-01 00:00:00",
                    "seller_memo": "好的",
                    "buyer_memo": "上衣要大一号"
                }
            }
        }

        if "open_trade_get_response" in test_order.keys():
            if "trade" in test_order["open_trade_get_response"]:
                return test_order["open_trade_get_response"]["trade"]
            return None