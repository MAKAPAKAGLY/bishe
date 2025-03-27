
from rest_framework.views import APIView
import random
from business.models import *
from system.models import *
from system.utils.json_response import *
import string
import uuid
import hashlib


# 用户注册
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if (serializer.is_valid()):
            if (User.objects.filter(username=request.data['username']).exists()):
                return ErrorResponse(msg="用户已存在")

            if 'name' not in request.data:
                name = request.data['username']
            else:
                name = request.data['name']
            # 生成uuid
            uid = uuid.uuid1()
            password = request.data['password']
            md5 = hashlib.md5()
            md5.update(password.encode('utf-8'))
            hashed_password = md5.hexdigest()
            serializer.save(name=name, uid=uid, password=hashed_password)

            user = User.objects.get(uid=uid)
            if request.data['role'] == 'MEMBER':
                Member.objects.create(username=request.data['username'],user_id=user.id,name=name)
            return SuccessResponse(msg="注册成功")
        else:
            return ErrorResponse(msg="数据验证失败")