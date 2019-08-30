from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#Character
class Character(models.Model):
    num = models.AutoField(primary_key=True) #번호
    name = models.CharField(max_length=100, blank=True, null=True) #케릭터 이름
    level = models.IntegerField(default=0) #레벨
    img = models.CharField(max_length=100, blank=True, null=True)  # 이미지

#User(One to One 방식으로 확장)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # id #번호
    # username #아이디
    # password #비밀번호
    name = models.CharField(max_length=100, blank=True, null=True)  #사용자 이름
    level = models.IntegerField(default=0) #레벨
    exp = models.IntegerField(default=0) #경험치
    delegateTitle = models.CharField(max_length=100, blank=True, null=True) #대표칭호
    character_num = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True) #캐릭터
    location = models.CharField(max_length=100, blank=True, null=True) #유저의 위치

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#Prefrence
class Preference(models.Model):
    num = models.AutoField(primary_key=True) #번호
    name = models.CharField(max_length=100, blank=True, null=True) #취향명

#Title
class Title(models.Model):
    num = models.AutoField(primary_key=True) #번호
    name = models.CharField(max_length=100, blank=True, null=True) #취향명
    text = models.CharField(max_length=100, blank=True, null=True)  # 취향설명
    img = models.CharField(max_length=100, blank=True, null=True)  # 이미지

#Activity
class Activity(models.Model):
    num = models.AutoField(primary_key=True) #번호
    name = models.CharField(max_length=100, blank=True, null=True) #엑티비티 이름
    location = models.CharField(max_length=100, blank=True, null=True) #엑티비티 위치



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
    name = models.CharField(max_length=100, blank=True, null=True)
    period = models.DateField(Preference, null=True)
    reward = models.IntegerField(Preference, null=True)

#엑티비티들의 취향 목록
class Activity_Preference(models.Model):
    num = models.AutoField(primary_key=True) #번호
    user_num = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True)
    preference_num = models.ForeignKey(Preference, on_delete=models.SET_NULL, null=True)