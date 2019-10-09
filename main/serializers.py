from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import Activity, User, User_Preference, Preference, User_Activity, Title, Review, CharacterImage,Activity_Preference
import datetime
from datetime import timezone


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = ('num', 'name')


class ActivityPreferenceSerializer(serializers.ModelSerializer):
    preferences = PreferenceSerializer(many=True, read_only=True)

    class Meta:
        model = Activity_Preference
        fields = '__all__'
        depth = 1



class CharacterImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CharacterImage
        fields = ('level', 'img', 'character_num_id')

#엑티비티 데이터 직렬화
class UserActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = User_Activity
        fields = ('num', 'user_num', 'activity_num', 'questDone', 'reviewDone','doneTime')

#엑티비티 데이터 직렬화
class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = ('num', 'name', 'eventStartDate', 'eventEndDate', 'eventTime', 'eventPlace', 'discription', 'longitude', 'latitude', 'tel', 'img', 'grade')
        # fields = '__all__'
        read_only_fields = fields

#유저 데이터를 직렬화
class UserSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.postNum = validated_data.get('postNum', instance.postNum)
        instance.save()
        return instance

    # https://seulcode.tistory.com/199

    class Meta:
        model = User
        fields = ('id','username','nickName','address','postNum', 'level', 'exp', 'character_num', 'title_num', 'longitude', 'latitude')

#칭호 데이터를 직렬화
class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('num','name','text','img')

#유저 타이틀 직렬화
class UserTitleSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=True)
    title = TitleSerializer(many=True)

#리뷰 데이터 직렬화
class ReviewSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        #date = validated_data.pop('date', None) #validated_data는 Meta 클래스에 등록한 속성들만 추린 데이터(헷갈리면 디버깅해보자)
        user_nickName = validated_data.pop('user_nickName', None)
        text = validated_data.pop('text', None)
        grade = validated_data.pop('grade', None)
        activity_num = validated_data.pop('activity_num', None)
        user_id = validated_data.pop('user_id', None)

        instance = self.Meta.model(**validated_data) #Review 인스턴스 생성

        now = datetime.datetime.now()
        now_utc = now.replace(tzinfo=timezone.utc)
        now_local = now_utc.astimezone()

        instance.doneTime = now_local
        instance.user_nickName = user_nickName
        instance.text = text
        instance.grade = grade
        instance.activity_num_id = activity_num.num
        instance.user_num_id = user_id
        instance.save()

        return instance

    class Meta:
        model = Review
        fields = ('num', 'doneTime', 'user_nickName', 'text', 'grade', 'activity_num', 'user_num')

#엑티비티 리뷰 직렬화
class ActivityReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity,Review
        fields = '__all__'
    activity = ActivitySerializer(many=True)
    review = ReviewSerializer(many=True)

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
        longitude = validated_data.pop('longitude', None)
        latitude = validated_data.pop('latitude', None)

        instance = self.Meta.model(**validated_data) #User 인스턴스 생성
        if password is not None:
            instance.set_password(password)

        instance.nickName = nickName #새로 만든 User 인스턴스에 회원가입 정보 저장
        instance.postNum = postNum
        instance.address = address
        instance.character_num = character_num
        instance.longitude = longitude
        instance.latitude = latitude
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
        fields = ('id','token', 'username', 'password','nickName','address','postNum', 'level', 'exp', 'character_num','longitude','latitude')
        # fields = '__all__'