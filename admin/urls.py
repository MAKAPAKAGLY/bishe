"""admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.static import serve

from admin import settings
from system.base.dict import *
from system.base.file import *
from system.base.login import *
from system.base.notice import *
from system.base.permission import *
from system.base.register import *
from system.base.role import *
from system.base.user import *
from business.views.member import *
from business.views.category import *
from business.views.stock import *
from business.views.industry import *
from business.views.collect import *
from business.views.membertags import *
from business.views.comments import *
from business.views.stockdata import *
from business.views.banner import *
from business.views.front import *
from business.views.prediction import *
from business.views.recommend import *


urlpatterns = [
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('logout/<str:id>', LogoutView.as_view()),
    path('user', UserView.as_view(),name="user"),
    path('user/<int:pk>', UserView.as_view(), name='user_detail'),
    path('user/page', UserPageView.as_view(), name="user_page"),
    path('user/del/batch', UserBatchDeleteAPIView.as_view(),name="user_batch_delete"),
    path('user/export', UserExport.as_view(),name="user_export"),
    path('updateUser', UserInfoUpdate.as_view(),name="user_info_update"),
    path('password/change', UserUpdatePwd.as_view(),name="user_update_pwd"),
    path('role', RoleView.as_view(),name="role"),
    path('role/<int:pk>', RoleView.as_view(), name='role_detail'),
    path('role/page', RolePageView.as_view(), name="role_page"),
    path('role/del/batch', RoleBatchDeleteAPIView.as_view(), name="role_batch_delete"),
    path('role/export', RoleExport.as_view(),name="role_export"),
    path('permission', PermissionView.as_view(),name="permission"),
    path('permission/<int:pk>', PermissionView.as_view(), name='permission_delete'),
    path('permission/del/batch', PermissionBatchDeleteAPIView.as_view(), name="permission_batch_delete"),
    path('permission/export', PermissionExport.as_view(),name="permission_export"),
    path('dict', DictView.as_view(), name="dict"),
    path('dict/<int:pk>', DictView.as_view(), name='dict_detail'),
    path('dict/page', DictPageView.as_view(), name="dict_page"),
    path('dict/del/batch', DictBatchDeleteAPIView.as_view(), name="dict_batch_delete"),
    path('dict/export', DictExport.as_view(),name="dict_export"),
    path('file/upload', FileUploadView.as_view(),name="file_upload"),
    path('file/uploadImg', FileUploadEditorView.as_view(),name="file_upload_editor"),
    path('notice', NoticeView.as_view(), name="notice"),
    path('notice/<int:pk>', NoticeView.as_view(), name='notice_detail'),
    path('notice/page', NoticePageView.as_view(), name="notice_page"),
    path('notice/del/batch', NoticeBatchDeleteAPIView.as_view(), name="notice_batch_delete"),
    path('notice/export', NoticeExport.as_view(), name="notice_export"),

    # 用户
    path('member', MemberView.as_view(), name="member"),
    path('member/<int:pk>', MemberView.as_view(), name='member_detail'),
    path('member/page', MemberPageView.as_view(), name="member_page"),
    path('member/del/batch', MemberBatchDeleteAPIView.as_view(), name="member_batch_delete"),
    path('member/export', MemberExport.as_view(), name="member_export"),
    path('front/member/user/<int:userId>', getMemberByUserId.as_view(), name="getMemberByUserId"),
    path('front/member/update', UpdateMember.as_view(), name="UpdateMember"),

    # 股票市场类型
    path('category', CategoryView.as_view(), name="category"),
    path('category/<int:pk>', CategoryView.as_view(), name='category_detail'),
    path('category/page', CategoryPageView.as_view(), name="category_page"),
    path('category/del/batch', CategoryBatchDeleteAPIView.as_view(), name="category_batch_delete"),
    path('category/export', CategoryExport.as_view(), name="category_export"),
    path('front/category/update', UpdateCategory.as_view(), name="UpdateCategory"),
    # 股票数据
    path('stock', StockView.as_view(), name="stock"),
    path('stock/<int:pk>', StockView.as_view(), name='stock_detail'),
    path('stock/page', StockPageView.as_view(), name="stock_page"),
    path('stock/del/batch', StockBatchDeleteAPIView.as_view(), name="stock_batch_delete"),
    path('stock/export', StockExport.as_view(), name="stock_export"),
    path('front/stock/update', UpdateStock.as_view(), name="UpdateStock"),
    # 板块行业
    path('industry', IndustryView.as_view(), name="industry"),
    path('industry/<int:pk>', IndustryView.as_view(), name='industry_detail'),
    path('industry/page', IndustryPageView.as_view(), name="industry_page"),
    path('industry/del/batch', IndustryBatchDeleteAPIView.as_view(), name="industry_batch_delete"),
    path('industry/export', IndustryExport.as_view(), name="industry_export"),
    path('front/industry/update', UpdateIndustry.as_view(), name="UpdateIndustry"),
    # 股票收藏
    path('collect', CollectView.as_view(), name="collect"),
    path('collect/<int:pk>', CollectView.as_view(), name='collect_detail'),
    path('collect/page', CollectPageView.as_view(), name="collect_page"),
    path('collect/del/batch', CollectBatchDeleteAPIView.as_view(), name="collect_batch_delete"),
    path('collect/export', CollectExport.as_view(), name="collect_export"),
    path('front/collect/update', UpdateCollect.as_view(), name="UpdateCollect"),
    # 用户标签
    path('membertags', MembertagsView.as_view(), name="membertags"),
    path('membertags/<int:pk>', MembertagsView.as_view(), name='membertags_detail'),
    path('membertags/page', MembertagsPageView.as_view(), name="membertags_page"),
    path('membertags/del/batch', MembertagsBatchDeleteAPIView.as_view(), name="membertags_batch_delete"),
    path('membertags/export', MembertagsExport.as_view(), name="membertags_export"),
    path('front/membertags/update', UpdateMembertags.as_view(), name="UpdateMembertags"),
    # 股票评论
    path('comments', CommentsView.as_view(), name="comments"),
    path('comments/<int:pk>', CommentsView.as_view(), name='comments_detail'),
    path('comments/page', CommentsPageView.as_view(), name="comments_page"),
    path('comments/del/batch', CommentsBatchDeleteAPIView.as_view(), name="comments_batch_delete"),
    path('comments/export', CommentsExport.as_view(), name="comments_export"),
    path('front/comments/update', UpdateComments.as_view(), name="UpdateComments"),
    # 股票价格数据
    path('stockdata', StockdataView.as_view(), name="stockdata"),
    path('stockdata/<int:pk>', StockdataView.as_view(), name='stockdata_detail'),
    path('stockdata/page', StockdataPageView.as_view(), name="stockdata_page"),
    path('stockdata/del/batch', StockdataBatchDeleteAPIView.as_view(), name="stockdata_batch_delete"),
    path('stockdata/export', StockdataExport.as_view(), name="stockdata_export"),
    path('front/stockdata/update', UpdateStockdata.as_view(), name="UpdateStockdata"),
	
    # 轮播图
    path('banner', BannerView.as_view(), name="banner"),
    path('banner/<int:pk>', BannerView.as_view(), name='banner_detail'),
    path('banner/page', BannerPageView.as_view(), name="banner_page"),
    path('banner/del/batch', BannerBatchDeleteAPIView.as_view(), name="banner_batch_delete"),
    path('banner/export', BannerExport.as_view(), name="banner_export"),

    # 前台-用户
    path('front/user/list', UserListDetail.as_view(), name="front_user_list"),
    path('front/user/<int:pk>', UserListDetail.as_view(), name='front_user_detail'),
    path('front/user/page', UserPage.as_view(), name="front_user_page"),
    # 前台-网站公告
    path('front/notice/list', NoticeListDetail.as_view(), name="front_notice_list"),
    path('front/notice/<int:pk>', NoticeListDetail.as_view(), name='front_notice_detail'),
    path('front/notice/page', NoticePage.as_view(), name="front_notice_page"),
    # 前台-轮播图
    path('front/banner/list', BannerListDetail.as_view(), name="front_banner_list"),
    path('front/banner', BannerListDetail.as_view(), name="front_banner"),
    path('front/banner/<int:pk>', BannerListDetail.as_view(), name='front_banner_detail'),
    path('front/banner/page', BannerPage.as_view(), name='front_banner_page'),
    # 前台-用户
    path('front/member/list', MemberListDetail.as_view(), name="front_member_list"),
    path('front/member', MemberListDetail.as_view(), name="front_member"),
    path('front/member/<int:pk>', MemberListDetail.as_view(), name='front_member_detail'),
    path('front/member/page', MemberPage.as_view(), name='front_member_page'),
    # 前台-股票市场类型
    path('front/category/list', CategoryListDetail.as_view(), name="front_category_list"),
    path('front/category', CategoryListDetail.as_view(), name="front_category"),
    path('front/category/<int:pk>', CategoryListDetail.as_view(), name='front_category_detail'),
    path('front/category/page', CategoryPage.as_view(), name='front_category_page'),
    # 前台-股票列表
    path('front/stock/list', StockListDetail.as_view(), name="front_stock_list"),
    path('front/stock', StockListDetail.as_view(), name="front_stock"),
    path('front/stock/<int:pk>', StockListDetail.as_view(), name='front_stock_detail'),
    path('front/stock/page', StockPage.as_view(), name='front_stock_page'),
    # 前台-板块行业
    path('front/industry/list', IndustryListDetail.as_view(), name="front_industry_list"),
    path('front/industry', IndustryListDetail.as_view(), name="front_industry"),
    path('front/industry/<int:pk>', IndustryListDetail.as_view(), name='front_industry_detail'),
    path('front/industry/page', IndustryPage.as_view(), name='front_industry_page'),
    # 前台-我的股票收藏
    path('front/collect/list', CollectListDetail.as_view(), name="front_collect_list"),
    path('front/collect', CollectListDetail.as_view(), name="front_collect"),
    path('front/collect/<int:pk>', CollectListDetail.as_view(), name='front_collect_detail'),
    path('front/collect/page', CollectPage.as_view(), name='front_collect_page'),
    # 前台-我的股票标签
    path('front/membertags/list', MembertagsListDetail.as_view(), name="front_membertags_list"),
    path('front/membertags', MembertagsListDetail.as_view(), name="front_membertags"),
    path('front/membertags/<int:pk>', MembertagsListDetail.as_view(), name='front_membertags_detail'),
    path('front/membertags/page', MembertagsPage.as_view(), name='front_membertags_page'),
    # 前台-股票评论
    path('front/comments/list', CommentsListDetail.as_view(), name="front_comments_list"),
    path('front/comments', CommentsListDetail.as_view(), name="front_comments"),
    path('front/comments/<int:pk>', CommentsListDetail.as_view(), name='front_comments_detail'),
    path('front/comments/page', CommentsPage.as_view(), name='front_comments_page'),
    # 前台-股票价格数据
    path('front/stockdata/list', StockdataListDetail.as_view(), name="front_stockdata_list"),
    path('front/stockdata/listbycode/<str:code>', StockdataListCodeDetail.as_view(), name="front_stockdatacode_list"),
    path('front/stockdata', StockdataListDetail.as_view(), name="front_stockdata"),
    path('front/stockdata/<int:pk>', StockdataListDetail.as_view(), name='front_stockdata_detail'),
    path('front/stockdata/page', StockdataPage.as_view(), name='front_stockdata_page'),




    #查看股票评论
    path('front/comments/tree', CommentsTree.as_view(), name="front_comments_tree"),
    #添加/修改股票评论
    path('front/comments/update', UpdateComments.as_view(), name="front_updatecomments"),



    # 股票收藏
    path('front/collect/update', UpdateCollect.as_view(), name="front_updateproducecollect"),
    path('front/collect/collect/<int:stockId>/<int:userId>', CheckCollect.as_view(), name="front_checkcollect"),
    path('front/collect/<int:stockId>/<int:userId>', DeleteCollect.as_view(), name="front_deletecollect"),

    # 修改浏览量
    path('front/stock/views/update/<int:id>', UpdateStockViews.as_view(), name="front_stockupdateviews"),

    # 添加推荐标签
    path('front/membertags/<int:categoryId>/<int:userId>', AddTags.as_view(), name="front_addtags"),
    # 删除推荐标签
    path('front/membertags/del/<int:categoryId>/<int:userId>', DeleteTags.as_view(), name="front_deletetags"),

    # 个性化推荐
    path('front/stockrecommend', UserRecommendView.as_view(), name="front_userrecommend"),

    # 统计-各股票市场数量统计
    path('statistics/categoryStatics', categoryStaticsView.as_view(), name="statistics_categoryStatics"),
    # 统计-各板块行业数量统计
    path('statistics/industryStatics', industryStaticsView.as_view(), name="statistics_industryStatics"),
    # 统计-各省份股票数量统计
    path('statistics/provinceStatics', provinceStaticsView.as_view(), name="statistics_provinceStatics"),

    # 统计-最新价走势图
    path('statistics/newpriceStatics/<str:code>', newpriceStaticsView.as_view(), name="statistics_newpriceStatics"),
    # 统计-成交量走势图
    path('statistics/turnoverStatics/<str:code>', turnoverStaticsView.as_view(), name="statistics_turnoverStatics"),
    # 统计-涨跌幅变化趋势
    path('statistics/chgStatics/<str:code>', chgStaticsView.as_view(), name="statistics_chgStatics"),

    # 股价预测
    path('front/predication', PredicationView.as_view(), name="front_predication"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
