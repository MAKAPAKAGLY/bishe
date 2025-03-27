from django.db.models import Count
from rest_framework.views import APIView
from business.models import *
from system.models import *
from system.utils.json_response import *
from system.utils.user import UserToken
from math import sqrt, pow
import operator
from django.db.models import Subquery, Q, Count


# 基于用户偏好相似度模型
class UserCf:

    # 获得初始化数据
    def __init__(self, all_user):
        self.all_user = all_user

    # 计算两个用户的皮尔逊相关系数
    def pearson(self, user1, user2):  # 数据格式为：物品id，浏览
        sum_xy = 0.0  # user1,user2 每项打分的的累加
        n = 0  # 公共浏览次数
        sum_x = 0.0  # user1 的打分总和
        sum_y = 0.0  # user2 的打分总和
        sumX2 = 0.0  # user1每项打分平方的累加
        sumY2 = 0.0  # user2每项打分平方的累加
        for data1, score1 in user1.items():
            if data1 in user2.keys():  # 计算公共的浏览次数
                n += 1
                sum_xy += score1 * user2[data1]
                sum_x += score1
                sum_y += user2[data1]
                sumX2 += pow(score1, 2)
                sumY2 += pow(user2[data1], 2)
        if n == 0:
            # print("p氏距离为0")
            return 0
        molecule = sum_xy - (sum_x * sum_y) / n  # 分子
        denominator = sqrt((sumX2 - pow(sum_x, 2) / n) * (sumY2 - pow(sum_y, 2) / n))  # 分母
        if denominator == 0:
            return 0
        r = molecule / denominator
        return r

    # 计算与当前用户的距离，获得最临近的用户
    def nearest_user(self, current_user, n=1):
        distances = {}
        # 用户，相似度
        # 遍历整个数据集
        for user in self.all_user.keys():
            # 非当前的用户
            if user != current_user:
                distance = self.pearson(self.all_user[current_user], self.all_user[user])
                # 计算两个用户的相似度
                distances[user] = distance
        closest_distance = sorted(
            distances.items(), key=operator.itemgetter(1), reverse=True
        )
        # 最相似的N个用户
        print("选取相似用户:", closest_distance[:n])
        return closest_distance[:n]

    # 给用户推荐数据
    def recommend(self, username, n=3):
        recommend = {}
        nearest_user = self.nearest_user(username, n)
        for user, score in dict(nearest_user).items():  # 最相近的n个用户
            for data, scores in self.all_user[user].items():  # 推荐的用户的数据列表
                if data not in self.all_user[username].keys():  # 当前username没有看过
                    if data not in recommend.keys():  # 添加到推荐列表中
                        recommend[data] = scores * score
        return sorted(recommend.items(), key=operator.itemgetter(1), reverse=True)


# 基于用户的推荐
class UserRecommendView(APIView):
    def get(self, request):
        # 获取当前登录用户
        user_id = UserToken.user_id(request)
        current_user = User.objects.get(id=user_id)

        # 查看用户是否评分
        comment_count = Comments.objects.filter(user_id=user_id).count()
        # 查看用户是否选择标签
        tags_list = Membertags.objects.filter(user_id=user_id).values_list('industry_id')
        # 没有评分
        if comment_count == 0:
            if len(tags_list) != 0:
                # 取出用户选择标签下的15个推荐数据
                recommend_list = Stock.objects.filter(industry_id__in=tags_list).order_by("-views")[:15]
            else:
                # 取出高浏览量的前15个数据
                recommend_list = Stock.objects.order_by("-views")[:15]
            serializerList = StockSerializer(recommend_list, many=True)
            return SuccessResponse(data=serializerList.data)

        # 取出评分数量前10的用户
        top_rated_users = Comments.objects.values('user_id').annotate(comment_count=Count('id')).order_by(
            '-comment_count')[:10]
        user_id_list = [user['user_id'] for user in top_rated_users]
        users = User.objects.filter(id__in=user_id_list)  # users评分最多的10个用户
        all_user = {}
        for user in users:
            # 找出每个用户的评分数据
            comments = Comments.objects.filter(user_id=user.id)
            rate = {}
            if comments:
                # 填充评分数据
                for i in comments:
                    rate.setdefault(str(i.stock_id), i.score)
                all_user.setdefault(user.username, rate)
            else:
                # 用户没有打过分，设为0
                all_user.setdefault(user.username, {})

        # 计算用户偏好相似度
        user_cf = UserCf(all_user=all_user)
        print('正在进行协同过滤算法推荐...')
        # 实施推荐
        recommend_list = [each[0] for each in user_cf.recommend(current_user.username, 15)]
        print('推荐结果为：')
        print(recommend_list)
        # 得到推荐的数据
        data_list = list(Stock.objects.filter(id__in=recommend_list).order_by("-views")[:15])
        # 推荐数据不足15个，则补充当前用户评价过的数据到数据集中，补充到15个为止
        other_length = 15 - len(data_list)
        if other_length > 0:
            id_list = Comments.objects.filter(user_id=user_id).values_list('stock_id')
            fix_list = Stock.objects.filter(id__in=id_list).order_by('-views')
            print('补充数据：')
            for item in fix_list:
                print(item.name)
            for fix in fix_list:
                if fix not in data_list:
                    data_list.append(fix)
                if len(data_list) >= 15:
                    break

        # 填充数据还不足15个的情况下，继续填充用户喜欢标签下的随机数据
        if len(data_list) < 15:
            need_length = 15 - len(data_list)
            last_recomm_list = Stock.objects.filter(industry_id__in=tags_list).order_by("-views")[:need_length]
            for recomm in last_recomm_list:
                data_list.append(recomm)

        serializerList = StockSerializer(data_list, many=True)
        print('最终展示数据结果：')
        for item in data_list:
            print(str(item.id) + " " + item.name)
        return SuccessResponse(data=serializerList.data)
