import hashlib
import json
import string
import uuid
import random
from datetime import datetime

import bcrypt
from django.apps import apps
from django.core.paginator import Paginator
from django.http import HttpResponse
from openpyxl import Workbook
from pytz import timezone
from rest_framework import status
from rest_framework.views import APIView
from system.models import *
from system.utils.json_response import *

#数据字典
class DictView(APIView):

    #查询
    def get(self, request, pk=None):
        if pk is None:
            dicts = SysDict.objects.all()
            serializerList = SysDictSerializer(dicts, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            dict = SysDict.objects.get(id=pk)
            serializer = SysDictSerializer(dict)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = SysDictSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            dict = SysDict.objects.get(pk=request.data['id'])
        except SysDict.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SysDictSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.update(dict,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        dict = SysDict.objects.filter(id=pk)
        dict.delete()
        return SuccessResponse(msg="删除成功")

# 分页
class DictPageView(APIView):

    # 查询数据
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        dicts = SysDict.objects.all().order_by('-id')
        if name:
            dicts = dicts.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(dicts, pageSize)
        list = paginator.page(pageNum)
        serializerList = SysDictSerializer(list,many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )

class DictBatchDeleteAPIView(APIView):
    def post(self, request):
        ids = request.data
        try:
            # 批量删除用户
            SysDict.objects.filter(id__in=ids).delete()
            return SuccessResponse(msg="删除成功")
        except:
            return ErrorResponse(msg="删除失败")


class DictExport(APIView):
    model = SysDict
    queryset = model.objects.all()
    serializer_class = SysDictSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Dict.xlsx"'

        # 创建Excel工作簿和工作表
        wb = Workbook()
        sheet = wb.active

        SysDict = apps.get_model('system','SysDict')
        fields = SysDict._meta.get_fields()
        fields = [field for field in fields if not field.is_relation]
        headers = [field.verbose_name for field in fields if field.concrete]
        sheet.append(headers)
        list = SysDict.objects.all()
        for data in list:
            sheet_data = []
            for field in fields:
                if field.concrete:
                    value = getattr(data, field.name)
                    if isinstance(value, datetime) and value.tzinfo:
                        value = value.astimezone(timezone('UTC'))
                        value = value.replace(tzinfo=None)
                    sheet_data.append(value)
            sheet.append(sheet_data)
        wb.save(response)
        return response