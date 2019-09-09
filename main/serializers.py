from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
#from django.contrib.auth.models import User
from .models import Activity, User


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = ('name', 'eventStartDate', 'eventEndDate', 'eventTime', 'eventPlace', 'discription', 'mapx', 'mapy', 'tel', 'img')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','level','address', 'exp')


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        nickName = validated_data.pop('nickName', None)
        postNum = validated_data.pop('postNum', None)
        address = validated_data.pop('address', None)
        #character_num = validated_data.pop('character_num', None)
        #tag = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.nickName=nickName
        instance.postNum=postNum
        instance.address=address
        #instance.character_num=character_num
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password','nickName','postNum','address','character_num','level', 'exp')