import re

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    ret = {
        "message": 'OK',
        'code': 1,
        "status": 2,
    }
    data_dict = {
        'user_id': user.id,
        'username': user.username,
        'token': token
    }
    ret['data'] = data_dict
    return ret


# 自定义Django的认证后端类
from django.contrib.auth.backends import ModelBackend


def get_user_by_account(account):
    """

    :param account: 手机号或者用户名
    :return:
    """
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """

        :param request:
        :param username: 用户名或者手机
        :param password:
        :param kwargs:
        :return:
        """
        # 根据用户名货手机号查询账户信息
        user = get_user_by_account(username)
        # 校验账户是否正确
        if user and user.check_password(password):
            return user
