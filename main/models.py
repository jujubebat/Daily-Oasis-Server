from django.db import models
from django.contrib.auth.models import AbstractUser

#Character
class Character(models.Model):
    num = models.AutoField(primary_key=True) #번호
    name = models.CharField(max_length=100, blank=True, null=True) #케릭터 이름
    level = models.IntegerField(default=0) #레벨
    img = models.CharField(max_length=100, blank=True, null=True)  # 이미지

#Title(칭호)
class Title(models.Model):
    num = models.AutoField(primary_key=True) #번호
    name = models.CharField(max_length=100, blank=True, null=True) #취향명
    text = models.CharField(max_length=100, blank=True, null=True)  # 취향설명
    img = models.CharField(max_length=100, blank=True, null=True)  # 이미지

class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)  # 사용자 이름
    nickName = models.CharField(max_length=100, blank=True, null=True)  # 닉네임
    address = models.CharField(max_length=100, blank=True, null=True)  # 주소
    postNum = models.CharField(max_length=100, blank=True, null=True)  # 우편번호
    level = models.IntegerField(default=0)  # 레벨
    exp = models.IntegerField(default=0)  # 경험치
    character_num = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True)  # 캐릭터
    title_num = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True)

#Prefrence(취향)
class Preference(models.Model):
    num = models.AutoField(primary_key=True) #번호
    name = models.CharField(max_length=100, blank=True, null=True) #취향명

#Activity(엑티비티)
class Activity(models.Model):
    num = models.AutoField(primary_key=True) #번호
    name = models.CharField(max_length=100, blank=True, null=True) #엑티비티 이름
    eventStartDate = models.CharField(max_length=100, blank=True, null=True) #엑티비티 시작일
    eventEndDate = models.CharField(max_length=100, blank=True, null=True) #엑티비티 종료일
    eventTime = models.TextField(max_length=1000, blank=True, null=True) #엑티비티 시간
    eventPlace = models.TextField(max_length=1000, blank=True, null=True) #엑티비티 장소명
    discription = models.TextField(max_length=1000, blank=True, null=True)  # 엑티비티 설명
    mapx = models.DecimalField(max_digits=20, decimal_places=12, blank=True, null=True) #x좌표
    mapy = models.DecimalField(max_digits=20, decimal_places=12, blank=True, null=True) #y좌표
    tel = models.CharField(max_length=255, blank=True, null=True) #엑티비티 전화번호
    img = models.CharField(max_length=255, blank=True, null=True) #엑티비티 이미지

#유저들의 취향 목록
class User_Preference(models.Model):
    num = models.AutoField(primary_key=True) #번호
    user_num = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    preference_num = models.ForeignKey(Preference, on_delete=models.SET_NULL, null=True)

#유저들의 칭호 목록
class User_Title(models.Model):
    num = models.AutoField(primary_key=True) #번호
    user_num = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    preference_num = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True)

#유저들의 엑티비티 목록
class User_Activity(models.Model):
    num = models.AutoField(primary_key=True) #번호
    user_num = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    activity_num = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True)

#엑티비티들의 취향 목록
class Activity_Preference(models.Model):
    num = models.AutoField(primary_key=True) #번호
    user_num = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True)
    preference_num = models.ForeignKey(Preference, on_delete=models.SET_NULL, null=True)