from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer


class UserView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        ret = {
            'message': "OK"
        }
        # 1.接受参数，并校验
        serializer = self.get_serializer(data=request.data)
        # print(request.data)
        dad = serializer.is_valid(raise_exception=True)
        # print(dad)
        # 2. 创建新用户并保存用户信息<调用create的方法>
        serializer.save()
        # 3. 返回应答,注册成功
        ret["data"] = serializer.data
        return Response(ret, status=status.HTTP_200_OK)


class TestView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        ret = {
            'message': "OK"
        }
        ret['data'] = request.user.mobile
        print(request.user.id)
        users = User.objects.all()
        user_ = []
        for user in users:
            user_dict={}
            user_dict['id'] = user.id
            user_dict['mobile'] = user.mobile
            user_dict['username'] = user.username
            user_dict['is_activate'] = user.is_active

            user_.append(user_dict)
        ret['parm'] = request.data
        ret['user'] = user_
        print(ret)
        return Response(ret)
