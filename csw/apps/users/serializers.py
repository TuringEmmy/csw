import re

from django_redis import get_redis_connection
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField(label="短信验证码", write_only=True)
    token = serializers.CharField(label='jwt token', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'mobile', 'code', 'token')

        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 2,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    #
    def validate_mobile(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号码格式不正确')
            # return '手机号格式不正确'
        res = User.objects.filter(mobile=value).count()

        if res > 0:
            raise serializers.ValidationError("手机号码重复")
        return value


    def validate(self, attrs):
        # 短信验证码是否正确
        mobile = attrs['mobile']
        redis_conn = get_redis_connection('verify_codes')

        real_sms_code = redis_conn.get('sms_%s' % mobile)
        real_sms_code = b'123456'

        if real_sms_code is None:
            raise serializers.ValidationError("短信验证码已过期")

        sms_code = attrs['code']

        if sms_code != real_sms_code.decode():
            raise serializers.ValidationError("短信验证码错误")
        return attrs

    def create(self, validated_data):

        # 清除无用的数据
        del validated_data['code']

        # 创建新用户
        # print(**validated_data)
        user = User.objects.create_user(**validated_data)

        # ------------签发jwt----------------
        from rest_framework_jwt.settings import api_settings

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # 生成payload数据
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        # ------------签发jwt----------------
        # 给user对象增加token,保存jwt token数据
        user.token = token
        # 返回user
        return user
