import heapq
from recommend.SHAN import SHAN
from recommend.HRM import HRM
import recommend.Const as Const
from .models import MyItem
import torch


class RecommendModel:
    def __init__(self):
        embedding_size = Const.embedding_size
        drop_ratio = Const.drop_ratio
        num_users = Const.num_users
        num_items = Const.num_items
        self.topK = Const.topK
        self.dis_topK = Const.dis_topK
        # self.shan = torch.load('recommend/SHAN.pkl')
        self.shan = SHAN(num_users, num_items, embedding_size, drop_ratio)
        self.shan.load_state_dict(torch.load('recommend/SHAN_dict.pkl'))
        self.hrm = HRM(num_users, num_items, embedding_size, drop_ratio)

    @staticmethod
    def distance(item, latitude, longitude):
        la = abs(float(item.latitude) - latitude)
        lo = abs(float(item.longitude) - longitude)
        dis = pow(la, 2) + pow(lo, 2)
        return dis

    def get_result(self, user, L, S, latitude, longitude):
        # 只计算离当前位置最近的前200个地点
        item_db = MyItem.objects.all()
        dic = {}
        for item in item_db:
            dis = self.distance(item, float(latitude), float(longitude))
            dic[item.item_id] = dis
        item_set = heapq.nsmallest(self.dis_topK, dic, key=dic.get)

        map_item_score = {}
        user_var, L_var, S_var = [], [], []
        for i in range(0, item_set.__len__()):
            user_var.append(user)
            L_var.append(L)
            S_var.append(S)
        user_var = torch.LongTensor(user_var)
        L_var = torch.LongTensor(L_var)
        S_var = torch.LongTensor(S_var)
        item_var = torch.LongTensor(item_set)

        # 使用 SHAN 算法进行推荐
        if True:
            predictions = self.shan.forward(user_var, L_var, S_var, item_var)
        # 使用 HRM 算法进行推荐
        else:
            predictions = self.hrm.forward(user_var, L_var, S_var, item_var)

        for i in range(item_set.__len__()):
            item = item_set[i]
            map_item_score[item] = predictions.data.numpy()[i]
        rank_list = heapq.nlargest(self.topK, map_item_score, key=map_item_score.get)
        return rank_list
