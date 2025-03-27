import json
from datetime import datetime

from django.apps import apps
from django.core.paginator import Paginator
from django.http import HttpResponse
from openpyxl import Workbook
from pytz import timezone
from rest_framework import status
from rest_framework.views import APIView
from system.models import *
from system.utils.json_response import *


#角色
class RoleView(APIView):

    #查询
    def get(self, request, pk=None):
        if pk is None:
            roles = Role.objects.all()
            serializerList = RoleSerializer(roles, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            role = Role.objects.get(id=pk)
            serializer = RoleSerializer(role)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = RoleSerializer(data=request.data)

        permission_ids = request.data['permissionIds']
        permissions = Permission.objects.filter(id__in=permission_ids)

        if(serializer.is_valid()):
            serializer.save(permission=permissions)
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            role = Role.objects.get(pk=request.data['id'])
        except Role.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request_data = request.data.copy()
        request_data['permission'] = request_data['permissionIds']
        serializer = RoleSerializer(data=request_data)

        if(serializer.is_valid()):
            serializer.update(role,serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        role = Role.objects.filter(id=pk)
        role.delete()
        return SuccessResponse(msg="删除成功")

#分页
class RolePageView(APIView):

    # 查询数据
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        roles = Role.objects.all().order_by('-id')
        if name:
            roles = roles.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(roles, pageSize)
        list = paginator.page(pageNum)
        serializerList = RoleSerializer(list, many=True)
        return PageResponse(page=pageNum,
                                limit=pageSize,
                                total=paginator.count,
                                pages=paginator.num_pages,
                                data=serializerList.data
                                )

class RoleBatchDeleteAPIView(APIView):
    def post(self, request):
        ids = request.data
        try:
            Role.objects.filter(id__in=ids).delete()
            return SuccessResponse(msg="删除成功")
        except:
            return ErrorResponse(msg="删除失败")


class RoleExport(APIView):
    model = Role
    queryset = model.objects.all()
    serializer_class = RoleSerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Role.xlsx"'

        # 创建Excel工作簿和工作表
        wb = Workbook()
        sheet = wb.active

        Role = apps.get_model('system','Role')
        fields = Role._meta.get_fields()
        fields = [field for field in fields if not field.is_relation]
        headers = [field.verbose_name for field in fields if field.concrete]
        sheet.append(headers)
        list = Role.objects.all()
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