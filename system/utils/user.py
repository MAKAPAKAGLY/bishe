from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed

# 获取用户token数据
class UserToken():
    @staticmethod
    def user_id(request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header:
            raise AuthenticationFailed("未提供认证令牌")
            
        try:
            token = auth_header.split(' ')[1]
            access_token = AccessToken(token)
            payload = access_token.payload
            user_id = payload.get('user_id')
            if not user_id:
                raise AuthenticationFailed("无效的用户令牌")
            return user_id
        except IndexError:
            raise AuthenticationFailed("认证令牌格式错误")
        except Exception as e:
            raise AuthenticationFailed("无效的认证令牌")