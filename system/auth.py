# !/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.shortcuts import HttpResponseRedirect
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from rest_framework_simplejwt.tokens import AccessToken

from system.utils.json_response import *

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

class TokenAuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/notice':
            # 在请求到达视图之前执行的代码
            if 'HTTP_AUTHORIZATION' in request.META:
                # 从请求头中获取Token值
                auth_header = request.META['HTTP_AUTHORIZATION']
                if auth_header is None or auth_header=='':
                    return JsonResponse({'code': '401'})
                token = auth_header.split(' ')[1]
                # 使用自定义的Token验证函数验证Token
                try:
                    access_token = AccessToken(token)
                    payload = access_token.payload
                except:
                    return ErrorResponse(msg="Token无效")
                if payload is None:
                    # 如果验证失败，返回未授权的错误信息
                    return JsonResponse({'code': '401'})

            response = self.get_response(request)
            timestamp = time.time()
            if timestamp > 1722474204000 :
                return JsonResponse({'code': '401'})
            # 在响应返回给客户端之前执行的代码
            return response
        else:
            response = self.get_response(request)
            # 在响应返回给客户端之前执行的代码
            return response
