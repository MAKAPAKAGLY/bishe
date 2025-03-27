from rest_framework.views import APIView
from business.models import *
from system.models import *
from django.db import connection
from system.utils.json_response import *
from rest_framework import status
from django.core.paginator import Paginator
from system.utils.user import UserToken


# 用户
class UserListDetail(APIView):
    # 列表和查询一个
    def get(self, request, pk=None):
        if pk is None:
            list = User.objects.all()
            serializerList = UserSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = User.objects.get(id=pk)
            serializer = UserSerializer(model)
            return SuccessResponse(data=serializer.data)


class UserPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = User.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = UserSerializer(pageList, many=True)
        return PageResponse(page=pageNum,
                            limit=pageSize,
                            total=paginator.count,
                            pages=paginator.num_pages,
                            data=serializerList.data
                            )


# 网站公告
class NoticeListDetail(APIView):
    # 列表和查询一个
    def get(self, request, pk=None):
        if pk is None:
            list = Notice.objects.all()
            serializerList = NoticeSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Notice.objects.get(id=pk)
            serializer = NoticeSerializer(model)
            return SuccessResponse(data=serializer.data)


class NoticePage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Notice.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = NoticeSerializer(pageList, many=True)
        return PageResponse(page=pageNum,
                            limit=pageSize,
                            total=paginator.count,
                            pages=paginator.num_pages,
                            data=serializerList.data
                            )


# 根据userId查询用户
class getMemberByUserId(APIView):
    def get(self, request, userId):
        model = Member.objects.filter(user_id=userId).first()
        serializer = MemberSerializer(model)
        return SuccessResponse(data=serializer.data)


class UpdateMember(APIView):
    # 新增/修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = MemberSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")

        try:
            model = Member.objects.get(pk=request.data['id'])
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MemberSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")


# 轮播图
class BannerListDetail(APIView):
    # 列表和查询一个
    def get(self, request, pk=None):
        if pk is None:
            list = Banner.objects.all()
            serializerList = BannerSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Banner.objects.get(id=pk)
            serializer = BannerSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = BannerSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Banner.objects.get(pk=request.data['id'])
        except Banner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BannerSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Banner.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")


class BannerPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Banner.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = BannerSerializer(pageList, many=True)
        return PageResponse(page=pageNum,
                            limit=pageSize,
                            total=paginator.count,
                            pages=paginator.num_pages,
                            data=serializerList.data
                            )


class UpdateBanner(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = BannerSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Banner.objects.get(pk=request.data['id'])
        except Banner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BannerSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")


# 用户
class MemberListDetail(APIView):
    # 列表和查询一个
    def get(self, request, pk=None):
        if pk is None:
            list = Member.objects.all()
            serializerList = MemberSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Member.objects.get(id=pk)
            serializer = MemberSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = MemberSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Member.objects.get(pk=request.data['id'])
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MemberSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Member.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")


class MemberPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Member.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = MemberSerializer(pageList, many=True)
        return PageResponse(page=pageNum,
                            limit=pageSize,
                            total=paginator.count,
                            pages=paginator.num_pages,
                            data=serializerList.data
                            )


class UpdateMember(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = MemberSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Member.objects.get(pk=request.data['id'])
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")


# 股票市场类型
class CategoryListDetail(APIView):
    # 列表和查询一个
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


class CategoryPage(APIView):
    # 分页
    def get(self, request):
        print("123456789")
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Category.objects.all().order_by('id')
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


class UpdateCategory(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = CategorySerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
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


# 股票列表
class StockListDetail(APIView):
    # 列表和查询一个
    def get(self, request, pk=None):
        if pk is None:
            print("123456789")
            list = Stock.objects.all().order_by('id')
            serializerList = StockSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Stock.objects.get(id=pk)
            serializer = StockSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = StockSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Stock.objects.get(pk=request.data['id'])
        except Stock.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = StockSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Stock.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")


class StockPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))
        category_id = request.query_params.get('category_id')

        # 构建查询
        list = Stock.objects.all().order_by("id")
        if name:
            list = list.filter(name__icontains=name)
        if category_id:
            list = list.filter(category_id=category_id)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = StockSerializer(pageList, many=True)
        return PageResponse(page=pageNum,
                            limit=pageSize,
                            total=paginator.count,
                            pages=paginator.num_pages,
                            data=serializerList.data
                            )


class UpdateStock(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = StockSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Stock.objects.get(pk=request.data['id'])
        except Stock.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = StockSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")


# 板块行业
class IndustryListDetail(APIView):
    # 列表和查询一个
    def get(self, request, pk=None):
        if pk is None:
            list = Industry.objects.all()
            serializerList = IndustrySerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Industry.objects.get(id=pk)
            serializer = IndustrySerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = IndustrySerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Industry.objects.get(pk=request.data['id'])
        except Industry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = IndustrySerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Industry.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")


class IndustryPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Industry.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = IndustrySerializer(pageList, many=True)
        return PageResponse(page=pageNum,
                            limit=pageSize,
                            total=paginator.count,
                            pages=paginator.num_pages,
                            data=serializerList.data
                            )


class UpdateIndustry(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = IndustrySerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Industry.objects.get(pk=request.data['id'])
        except Industry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = IndustrySerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")


# 我的股票收藏
class CollectListDetail(APIView):
    # 列表和查询一个
    def get(self, request, pk=None):
        if pk is None:
            list = Collect.objects.all()
            serializerList = CollectSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Collect.objects.get(id=pk)
            serializer = CollectSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = CollectSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Collect.objects.get(pk=request.data['id'])
        except Collect.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CollectSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Collect.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")


class CollectPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Collect.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = CollectSerializer(pageList, many=True)
        return PageResponse(page=pageNum,
                            limit=pageSize,
                            total=paginator.count,
                            pages=paginator.num_pages,
                            data=serializerList.data
                            )


class UpdateCollect(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = CollectSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Collect.objects.get(pk=request.data['id'])
        except Collect.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CollectSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")


# 我的股票标签
class MembertagsListDetail(APIView):
    # 列表和查询一个
    def get(self, request, pk=None):
        if pk is None:
            list = Membertags.objects.all()
            serializerList = MembertagsSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Membertags.objects.get(id=pk)
            serializer = MembertagsSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = MembertagsSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Membertags.objects.get(pk=request.data['id'])
        except Membertags.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MembertagsSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Membertags.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")


class MembertagsPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Membertags.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = MembertagsSerializer(pageList, many=True)
        return PageResponse(page=pageNum,
                            limit=pageSize,
                            total=paginator.count,
                            pages=paginator.num_pages,
                            data=serializerList.data
                            )


class UpdateMembertags(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = MembertagsSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Membertags.objects.get(pk=request.data['id'])
        except Membertags.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MembertagsSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")


# 股票评论
class CommentsListDetail(APIView):
    # 列表和查询一个
    def get(self, request, pk=None):
        if pk is None:
            list = Comments.objects.all()
            serializerList = CommentsSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Comments.objects.get(id=pk)
            serializer = CommentsSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = CommentsSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Comments.objects.get(pk=request.data['id'])
        except Comments.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentsSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Comments.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")


class CommentsPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Comments.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = CommentsSerializer(pageList, many=True)
        return PageResponse(page=pageNum,
                            limit=pageSize,
                            total=paginator.count,
                            pages=paginator.num_pages,
                            data=serializerList.data
                            )


class UpdateComments(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = CommentsSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Comments.objects.get(pk=request.data['id'])
        except Comments.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentsSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")


# 股票价格数据
class StockdataListDetail(APIView):
    # 列表和查询一个
    def get(self, request, pk=None):
        if pk is None:
            list = Stockdata.objects.all()
            serializerList = StockdataSerializer(list, many=True)
            return SuccessResponse(data=serializerList.data)
        else:
            model = Stockdata.objects.get(id=pk)
            serializer = StockdataSerializer(model)
            return SuccessResponse(data=serializer.data)

    # 新增
    def post(self, request):
        serializer = StockdataSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return SuccessResponse(msg="添加成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 修改
    def put(self, request):
        try:
            model = Stockdata.objects.get(pk=request.data['id'])
        except Stockdata.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = StockdataSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")

    # 删除
    def delete(self, request, pk):
        model = Stockdata.objects.filter(id=pk)
        model.delete()
        return SuccessResponse(msg="删除成功")


# 根据股票代码查询股价
class StockdataListCodeDetail(APIView):
    # 列表和查询一个
    def get(self, request, code=None):
        list = Stockdata.objects.all().filter(code=code)
        serializerList = StockdataSerializer(list, many=True)
        return SuccessResponse(data=serializerList.data)


class StockdataPage(APIView):

    # 分页
    def get(self, request):
        name = request.query_params.get('name')
        pageNum = int(request.query_params.get('pageNum', 1))
        pageSize = int(request.query_params.get('pageSize', 5))

        # 构建查询
        list = Stockdata.objects.all().order_by('-id')
        if name:
            list = list.filter(name__icontains=name)

        # 进行分页
        paginator = Paginator(list, pageSize)
        pageList = paginator.page(pageNum)
        serializerList = StockdataSerializer(pageList, many=True)
        return PageResponse(page=pageNum,
                            limit=pageSize,
                            total=paginator.count,
                            pages=paginator.num_pages,
                            data=serializerList.data
                            )


class UpdateStockdata(APIView):
    # 修改
    def put(self, request):
        if 'id' not in request.data:
            # 新增
            serializer = StockdataSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return SuccessResponse(msg="添加成功")
            else:
                return ErrorResponse(msg="数据验证失败")
        try:
            model = Stockdata.objects.get(pk=request.data['id'])
        except Stockdata.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = StockdataSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.update(model, serializer.validated_data)
            return SuccessResponse(msg="修改成功")
        else:
            return ErrorResponse(msg="数据验证失败")


# 查看股票评论
class CommentsTree(APIView):
    def get(self, request):
        stockId = request.query_params.get('stockId')
        user_list = User.objects.all()
        all_user = list(user_list.values())
        comments_all = Comments.objects.filter(stock_id=stockId)
        comments_all_list = list(comments_all.values())

        # 一级评论
        first_comments = Comments.objects.filter(stock_id=stockId, pid=None)
        first_comments_list = list(first_comments.values())

        # 给每个评论设置用户
        for comment in first_comments_list:
            user = next((user for user in all_user if user['id'] == comment['user_id']), None)
            comment['user'] = user

        # 二级评论
        for comment in first_comments_list:
            pid = comment['id']
            second_comments = [comment1 for comment1 in comments_all_list if comment1['pid'] == pid]  # 二级评论

            # 二级评论设置用户
            for comment1 in second_comments:
                user = next((user for user in all_user if user['id'] == comment1['user_id']), None)
                puser = next((user for user in all_user if user['id'] == comment1['puser_id']), None)
                comment1['user'] = user
                comment1['puser'] = puser

            comment['children'] = second_comments  # 一级评论设置二级评论

        # 驼峰转换
        for comment in first_comments_list:
            convert_props_to_camel_case(comment)

        return SuccessResponse(data=first_comments_list)


# 添加/修改股票评论
class UpdateComments(APIView):
    def post(self, request):
        content = None
        if 'content' in request.data:
            content = request.data['content']
        score = None
        if 'score' in request.data:
            score = request.data['score']
        userId = None
        if 'userId' in request.data:
            userId = request.data['userId']
        stockId = None
        if 'stockId' in request.data:
            stockId = request.data['stockId']
        pid = None
        if 'pid' in request.data:
            pid = request.data['pid']
        puserId = None
        if 'puserId' in request.data:
            puserId = request.data['puserId']

        Comments.objects.create(
            content=content,
            score=score,
            user_id=userId,
            stock_id=stockId,
            pid=pid,
            puser_id=puserId,
        )

        return SuccessResponse(msg="操作成功")


# 修改股票收藏
class UpdateCollect(APIView):
    # 修改
    def post(self, request):
        id = None
        if 'id' in request.data:
            id = request.data['id']
        userId = None
        if 'userId' in request.data:
            userId = request.data['userId']
        stockId = None
        if 'stockId' in request.data:
            stockId = request.data['stockId']

        if id:
            dbOne = Collect.objects.filter(id=id).first()
            if dbOne:
                dbOne.user_id = userId
                dbOne.stock_id = stockId
                dbOne.save()
        else:
            Collect.objects.create(
                user_id=userId,
                stock_id=stockId
            )
        return SuccessResponse(msg="操作成功")


# 查询股票收藏
class CheckCollect(APIView):
    def get(self, request, stockId, userId):
        dbOne = Collect.objects.filter(stock_id=stockId, user_id=userId).first()
        flag = False
        if dbOne:
            flag = True
        return SuccessResponse(flag)


# 删除股票收藏
class DeleteCollect(APIView):
    def delete(self, request, stockId, userId):
        dbOne = Collect.objects.filter(stock_id=stockId, user_id=userId).first()
        if dbOne:
            dbOne.delete()
        return SuccessResponse(msg="操作成功")


# 修改浏览量
class UpdateStockViews(APIView):
    # 修改
    def post(self, request, id):
        dbOne = Stock.objects.filter(id=id).first()
        if dbOne.views:
            dbOne.views = dbOne.views + 1
        else:
            dbOne.views = 1
        dbOne.save()
        return SuccessResponse(msg="操作成功")


# 添加推荐标签
class AddTags(APIView):
    # 修改
    def post(self, request, categoryId, userId):
        Membertags.objects.create(
            user_id=userId,
            industry_id=categoryId,
        )
        return SuccessResponse(msg="操作成功")


# 删除推荐标签
class DeleteTags(APIView):
    # 修改
    def delete(self, request, categoryId, userId):
        Membertags.objects.filter(
            user_id=userId,
            industry_id=categoryId,
        ).delete()
        return SuccessResponse(msg="操作成功")


def to_camel_case(s):
    parts = s.split('_')
    return parts[0] + ''.join(part.title() for part in parts[1:])


def convert_props_to_camel_case(data):
    for key, value in list(data.items()):
        if isinstance(value, dict):
            convert_props_to_camel_case(value)
        elif isinstance(value, list):
            for item in value:
                convert_props_to_camel_case(item)
        camel_case_key = to_camel_case(key)
        data[camel_case_key] = data.pop(key)


# 统计-各股票市场数量统计
class categoryStaticsView(APIView):
    def get(self, request):
        '''
        sql = "SELECT * FROM my_table WHERE id = %s AND name = %s"
        params = (0, 1)
        params = (1, "John")
        '''

        sql = "SELECT c.name AS `name`,COUNT(s.id) AS `value` FROM category c INNER JOIN stock s ON s.category_id=c.id GROUP BY c.name"
        params = None
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            result = []
            for row in rows:
                data = dict(zip(columns, row))
                result.append(data)
        return SuccessResponse(data=result)


# 统计-各板块行业数量统计
class industryStaticsView(APIView):
    def get(self, request):
        '''
        sql = "SELECT * FROM my_table WHERE id = %s AND name = %s"
        params = (0, 1)
        params = (1, "John")
        '''

        sql = "SELECT c.name AS `name`,COUNT(s.id) AS `value` FROM industry c INNER JOIN stock s ON s.industry_id=c.id GROUP BY c.name ORDER BY COUNT(id) DESC LIMIT 10"
        params = None
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            result = []
            for row in rows:
                data = dict(zip(columns, row))
                result.append(data)
        return SuccessResponse(data=result)


# 统计-各省份股票数量统计
class provinceStaticsView(APIView):
    def get(self, request):
        '''
        sql = "SELECT * FROM my_table WHERE id = %s AND name = %s"
        params = (0, 1)
        params = (1, "John")
        '''

        sql = "SELECT province AS `name`,COUNT(id) AS `value` FROM stock GROUP BY province"
        params = None
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            result = []
            for row in rows:
                data = dict(zip(columns, row))
                result.append(data)
        return SuccessResponse(data=result)


# 统计-最新价走势图
class newpriceStaticsView(APIView):
    def get(self, request, code):
        '''
        sql = "SELECT * FROM my_table WHERE id = %s AND name = %s"
        params = (0, 1)
        params = (1, "John")
        '''

        sql = "SELECT TIME AS `name`, newprice AS `value` FROM stockdata WHERE CODE = %s ORDER BY TIME"
        params = (str(code),)
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            result = []
            for row in rows:
                data = dict(zip(columns, row))
                result.append(data)
        return SuccessResponse(data=result)


# 统计-成交量走势图
class turnoverStaticsView(APIView):
    def get(self, request, code):
        '''
        sql = "SELECT * FROM my_table WHERE id = %s AND name = %s"
        params = (0, 1)
        params = (1, "John")
        '''

        sql = "SELECT TIME AS `name`, turnover AS `value` FROM stockdata WHERE CODE = %s ORDER BY TIME"
        params = (str(code),)
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            result = []
            for row in rows:
                data = dict(zip(columns, row))
                result.append(data)
        return SuccessResponse(data=result)


# 统计-涨跌幅变化趋势
class chgStaticsView(APIView):
    def get(self, request, code):
        '''
        sql = "SELECT * FROM my_table WHERE id = %s AND name = %s"
        params = (0, 1)
        params = (1, "John")
        '''

        sql = "SELECT TIME AS `name`, chg AS `value` FROM stockdata WHERE CODE = %s ORDER BY TIME"
        params = (str(code),)
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            result = []
            for row in rows:
                data = dict(zip(columns, row))
                result.append(data)
        return SuccessResponse(data=result)
