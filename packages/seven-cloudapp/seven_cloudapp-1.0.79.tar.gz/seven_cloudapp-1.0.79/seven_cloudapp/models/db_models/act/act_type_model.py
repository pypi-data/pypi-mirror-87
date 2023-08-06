
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class ActTypeModel(BaseModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None):
        super(ActTypeModel, self).__init__(ActType, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction

    #方法扩展请继承此类
    
class ActType:

    def __init__(self):
        super(ActType, self).__init__()
        self.id = 0  # id
        self.type_name = ""  # 类型名称
        self.act_title = ""  # 活动标题
        self.act_img = ""  # 活动图
        self.marketing_id = ""  # 营销方案id列表（逗号分隔多个id）
        self.experience_img = ""  # 体验码二维码图
        self.play_process = ""  # 玩法流程
        self.applicable_behavior = ""  # 适用行为
        self.market_function = ""  # 营销功能
        self.skill_case = ""  # 活动设置技巧案例
        self.currency_type = 0  # （0无1次数2积分3价格档位4抽奖码）
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 更新时间

    @classmethod
    def get_field_list(self):
        return ['id', 'type_name', 'act_title', 'act_img', 'marketing_id', 'experience_img', 'play_process', 'applicable_behavior', 'market_function', 'skill_case', 'currency_type', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "act_type_tb"
    