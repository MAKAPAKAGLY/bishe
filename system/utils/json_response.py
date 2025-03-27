# -*- coding: utf-8 -*-


from rest_framework.response import Response

class SuccessResponse(Response):

    def __init__(self, data=None, msg='操作成功', code="200", status=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        std_data = {
            "code": code,
            "data": data,
            "msg": msg
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)


class PageResponse(Response):
    def __init__(self, data=None, msg='success', status=None, template_name=None, headers=None, exception=False,
                 content_type=None,page=1,limit=1,total=1,pages=1):
        std_data = {
            "code": "200",
            "data": {
                "current": page,
                "size": limit,
                "total": total,
                "records": data,
                "pages": pages
            },
            "msg": msg
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)


class DataResponse(Response):

    def __init__(self, data=None, msg='success', status=None, template_name=None, headers=None, exception=False,
                 content_type=None,):
        std_data = {
            "code": "200",
            "data": data,
            "msg": msg
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)


class ErrorResponse(Response):

    def __init__(self, data=None, msg='error', code="400", status=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        std_data = {
            "code": code,
            "data": data,
            "msg": msg
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)
