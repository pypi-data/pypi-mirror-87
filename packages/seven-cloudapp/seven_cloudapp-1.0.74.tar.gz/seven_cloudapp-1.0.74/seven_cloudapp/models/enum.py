# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-06-02 14:32:40
@LastEditTime: 2020-12-01 16:21:59
@LastEditors: HuangJingCan
@Description: 枚举类
"""

from enum import Enum, unique


class TagType(Enum):
    """
    @description: 标签类型
    """
    无 = 0
    限定 = 1
    稀有 = 2
    绝版 = 3
    隐藏 = 4


class SourceType(Enum):
    """
    @description: 用户次数配置来源类型
    """
    购买 = 1
    任务 = 2
    手动配置 = 3


class OperationType(Enum):
    """
    @description: 用户操作日志类型
    """
    add = 1
    update = 2
    delete = 3


class TaskType(Enum):
    """
    docstring：任务类型
    """
    # {"reward_value":0}
    新人有礼 = 1
    # {"reward_value":0}
    每日签到 = 2
    # {"reward_value":0,"user_limit":0}
    邀请新用户 = 3
    # {"reward_value":0}
    关注店铺 = 4
    # {"reward_value":0}
    加入店铺会员 = 5
    # {"reward_value":0,"num_limit":0,"effective_date_start":'1900-01-01 00:00:00',"effective_date_end":'1900-01-01 00:00:00',"goods_ids":"","goods_list":[]}
    下单购买指定商品 = 6
    # {"reward_value":0,"num_limit":0,"goods_ids":"","goods_list":[]}
    收藏商品 = 7
    # {"reward_value":0,"num_limit":0,"goods_ids":"","goods_list":[]}
    浏览商品 = 8
    # {"reward_value":0,"join_type":（1商家群链接2选择单群聊）,"join_url":"","chatting_id":"","chatting_name":""}
    加入群聊 = 9
    # {"reward_value":0,"chatting_id":"","chatting_name":""}
    分享群聊 = 10
    # 云应用未开放此功能
    直播 = 11
    # {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0}
    每周签到 = 12
    # {"reward_value":0,"effective_date_start":'1900-01-01 00:00:00',"effective_date_end":'1900-01-01 00:00:00'}
    下单任意消费 = 13
    # {"effective_date_start":'1900-01-01 00:00:00',"effective_date_end":'1900-01-01 00:00:00',"reward_list":[{"key":"前端算唯一值","money":500,"reward_value":0}]}
    累计消费 = 14
    # {"effective_date_start":'1900-01-01 00:00:00',"effective_date_end":'1900-01-01 00:00:00',"reward_list":[{"key":"前端算唯一值","money":500,"reward_value":0}]}
    单笔订单消费 = 15
    # 从活动奖品表配置
    店长好礼 = 16
