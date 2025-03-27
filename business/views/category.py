from datetime import datetime

from django.apps import apps
from django.core.paginator import Paginator
from django.http import HttpResponse
from openpyxl import Workbook
from pytz import timezone
from rest_framework import status
from rest_framework.views import APIView

from business.models import *
from system.models import *
from system.utils.json_response import *
from system.utils.user import UserToken


# 股票市场类型
class CategoryView(APIView):

    # 查询数据
    def get(self, request, pk=None):
        if pk is None:
            list = Category.objects.all()
            serializerList = CategorySerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Category.objects.get(id=pk)
            serializer = CategorySerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Category.objects.get(pk=request.data['id'])
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Category.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")


# 分页
class CategoryPageView(APIView):

    # 查询数据
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        user_id = UserToken.user_id(request)
        user = User.objects.get(pk=user_id)

        # 构建查询
        list = Category.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = CategorySerializer(pageList, many=True)
        return PageResponse(page=pageNum,
                            limit=pageSize,
                            total=paginator.count,
                            pages=paginator.num_pages,
                            data=serializerList.data
                            )


class CategoryBatchDeleteAPIView(APIView):
    def post(self, request):
        ids = request.data
        try:
            Category.objects.filter(id__in=ids).delete()
            return SuccessResponse(msg="删除成功")
        except:
            return ErrorResponse(msg="删除失败")


class CategoryExport(APIView):
    model = Category
    queryset = model.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Category.xlsx"'

        # 创建Excel工作簿和工作表
        wb = Workbook()
        sheet = wb.active

        model = apps.get_model('business', 'Category')
        fields = model._meta.get_fields()
        fields = [field for field in fields if not field.is_relation]
        headers = [field.verbose_name for field in fields if field.concrete]
        sheet.append(headers)
        list = Category.objects.all()
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
