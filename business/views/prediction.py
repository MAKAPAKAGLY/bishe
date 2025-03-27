import os

from django.core.wsgi import get_wsgi_application
from django.db import connection
import pandas as pd
from rest_framework.views import APIView
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from system.utils.json_response import SuccessResponse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
application = get_wsgi_application()
import django
django.setup()

transfer = LabelEncoder()

# 获取数据集
def get_data():
    with connection.cursor() as cursor:
        cursor.execute('SELECT code,openprice,turnover,amount,newprice FROM stockdata')
        rows = cursor.fetchall()
        df = pd.DataFrame(rows,columns=['code', 'turnover','amount','openprice', 'newprice'])
        # 进行数据处理
        X = df[['code', 'turnover','amount','openprice', 'newprice']]
        X['code'] = transfer.fit_transform(X['code'].values)
        X['turnover'] = X['code'].astype('float')
        X['amount'] = X['amount'].astype('float')
        X['openprice'] = X['openprice'].astype('float')
        X['newprice'] = X['newprice'].astype('float')
    return X

# 训练数据集
def model_train():
    # 获取数据
    data = get_data()
    # 数据集 测试集划分
    x_train, x_test, y_train, y_test = train_test_split(data[['code', 'turnover','amount','openprice']], data['newprice'], test_size=0.25,random_state=1)
    # 创建一个线性回归对象
    model = LinearRegression()
    # 多元线性回归模型训练
    model.fit(x_train, y_train)
    return model

# 预测
def pred(model,code,turnover,openprice,amount):
    code = transfer.transform([code])[0]
    hots = model.predict([[code,turnover,amount,openprice]])
    return hots

# 开始预测
class PredicationView(APIView):
    def get(self, request):
        code = request.query_params.get('code')
        turnover = request.query_params.get('turnover')
        openprice = request.query_params.get('openprice')
        amount = request.query_params.get('amount')
        model = model_train()
        result = pred(model,code,turnover,openprice,amount)
        return SuccessResponse(data=round(result[0],1))
