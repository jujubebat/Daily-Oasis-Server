from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import Activity, User, User_Preference, Preference

#엑티비티 데이터 직렬화
class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = ('name', 'eventStartDate', 'eventEndDate', 'eventTime', 'eventPlace', 'discription', 'mapx', 'mapy', 'tel', 'img')

#유저 데이터를 직렬화
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','nickName','address','postNum', 'level', 'exp', 'character_num', 'title_num')

#유저 데이터 + 토큰정보 + 회원가입 관련 직렬화
class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    #토큰 발급
    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    #유저 모델 생성후 등록
    def create(self, validated_data):
        password = validated_data.pop('password', None) #validated_data는 Meta 클래스에 등록한 속성들만 추린 데이터(헷갈리면 디버깅해보자)
        nickName = validated_data.pop('nickName', None)
        postNum = validated_data.pop('postNum', None)
        address = validated_data.pop('address', None)
        character_num = validated_data.pop('character_num', None)

        instance= self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        instance.nickName = nickName
        instance.postNum = postNum
        instance.address = address
        instance.character_num = character_num
        instance.save()

        #유저에 태그 등록하는 부분
        #유저-선호(태그) 관계 테이블에 post로 받은 유저번호와 선호(태그) 배열 데이터들을 넣어줌
        tags = self.initial_data.pop('tag') #initial_data는 post로 받은 raw 데이터(헷갈리면 디버깅해보자)
        for tag in tags: #배열로 받은 태그 데이터를 하나하나 뽑음
            User_Preference_instance = User_Preference.objects.create()
            User_Preference_instance.user_num_id = instance
            User_Preference_instance.preference_num = Preference.objects.get(pk=tag)#태그에 해당하는 객체 불러서 외래키에 넣어줌
            User_Preference_instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password','nickName','address','postNum', 'level', 'exp', 'character_num')