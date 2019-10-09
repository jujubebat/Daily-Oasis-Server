from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas
import datetime
from datetime import timezone
from .serializers import UserSerializer, UserSerializerWithToken, ActivitySerializer, UserActivitySerializer, ReviewSerializer, TitleSerializer, CharacterImageSerializer,PreferenceSerializer,ActivityPreferenceSerializer
from .models import Activity, User_Preference, Preference, Activity_Preference, User_Activity, Title, User, User_Title, User_Character, Review, CharacterImage, Character
from django.db import transaction
from django.db.models import Avg
from scipy.spatial import distance
import pprint, re
from django.db.models import Count

#api.dailyoasis.shop

#현재 유저가 진행중인 퀘스트 목록(엑티비티) 리턴
class CurrentQuest(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        quests = User_Activity.objects.filter(user_num_id=request.user.id, questDone=0)
        quest_serializer = UserActivitySerializer(quests, many=True)

        list=[]
        for quest in quests:
            list.append(quest.activity_num.num)

        activity=Activity.objects.filter(pk__in=list)
        activity_serializer = ActivitySerializer(activity, many=True)

        activity_preference = Activity_Preference.objects.filter(activity_num_id__in=list)
        activity_preference_serializer= ActivityPreferenceSerializer(activity_preference, many=True)

        return Response({"CurrentQuest":quest_serializer.data, "CurrentActivity":activity_serializer.data , "ActivityPreference":activity_preference_serializer.data })

#유저가 완료한 퀘스트 제공(발자취)
class DoneQuest(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        quests = User_Activity.objects.filter(user_num_id=request.user.id, questDone=1)
        quest_serializer = UserActivitySerializer(quests, many=True)

        list = []
        for quest in quests:
            list.append(quest.activity_num.num)

        activity = Activity.objects.filter(pk__in=list)
        activity_serializer = ActivitySerializer(activity, many=True)

        activity_preference = Activity_Preference.objects.filter(activity_num_id__in=list)
        activity_preference_serializer = ActivityPreferenceSerializer(activity_preference, many=True)

        return Response({"DoneQuest": quest_serializer.data, "DoneActivity": activity_serializer.data, "ActivityPreference": activity_preference_serializer.data})


#유저가 보유한 타이틀 리턴
class UserTitle(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        user_title_items = User_Title.objects.filter(user_num_id = request.user.id)

        list = []
        for user_title_item in user_title_items:
            list.append(user_title_item.title_num_id)

        data = Title.objects.filter(pk__in = list)
        serializer = TitleSerializer(data, many=True)
        return Response({"UserTitleList": serializer.data})

#유저가 보유한 선호도(태그)리턴
class UserPreference(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        user_preference_items = User_Preference.objects.filter(user_num_id = request.user.id)

        list = []
        for user_preference_item in user_preference_items:
            list.append(user_preference_item.preference_num_id)

        data = Preference.objects.filter(pk__in = list)
        serializer = PreferenceSerializer(data, many=True)
        return Response({"UserTagList": serializer.data})

#모든 엑티비티 리스트 제공
class ActivityList(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        data = Activity.objects.all()
        serializer = ActivitySerializer(data, many=True)
        a=1
        return Response({"ActivityList" : serializer.data})#, "sadddsas" : serializer2.data})


#먼저 태그 배열에서 태그 목록 리스트 만듬
#엑티비티_프리퍼런스에서 태그목록을 모두 가지는 엑티비티만 추출해서 엑티비티 번호 리스트 만듬
#엑티비티 번호 리스트로 엑티비티 직렬화
#http://127.0.0.1:8000/activityListByPreference?tag1=0&tag2=0&tag3=0&tag4=0&tag5=0


class ActivityListByPreference(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):

        quest_num = request.query_params
        request_tag_dict = dict(quest_num.lists())
        request_tag = list(map(int,request_tag_dict['tag']))
        activity_list = []
        activity_items = Activity.objects.filter()
        activity_nums=activity_items.values_list('num', flat=True)
        b=1
        for activity_num in activity_nums:
            print(activity_num)
            activity_preference_items = Activity_Preference.objects.filter(activity_num_id=activity_num)
            activity_tag = []
            preference_nums= activity_preference_items.values_list('preference_num_id',flat=True)
            activity_tag=list(preference_nums)

            intersection = set([])
            intersection = set(request_tag).intersection(set(activity_tag))
            inter_list = list(intersection)
            inter_list.sort()
            if (request_tag == inter_list):
                print('포함합니다.')
                activity_list.append(activity_num)
        activity_preference_items = Activity_Preference.objects.all()
        for activity_preference_item in activity_preference_items:
            activity_tag.append(activity_preference_item.preference_num_id)

        print('끝')
        data = Activity.objects.filter(pk__in=activity_list)
        serializer = ActivitySerializer(data, many=True)
        print(data)
        return Response({"ActivityListByPreference" : serializer.data})

#모든 칭호 리스트 제공
class TitleList(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        data = Title.objects.all()
        serializer = TitleSerializer(data, many=True)
        return Response({"TitleList":serializer.data})

#모든 케릭터 리스트 제공
class CharacterList(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        data = Character.objects.all()
        character_serializer = ActivitySerializer(data, many=True)

        data = CharacterImage.objects.all()
        characterImangeList_serializer = CharacterImageSerializer(data, many=True)

        return Response({"CharacterList": character_serializer.data, "CharacterImageList": characterImangeList_serializer.data})

#Activity에 '소외된'(발걸음이_적은) 태그가 있는 경우 판별
def isAlienate(activity):
    activity_tags = Activity_Preference.objects.filter(activity_num_id=activity.pk)
    for activity_tag in activity_tags :
        tag = Preference.objects.get(pk=activity_tag.preference_num_id)
        if tag.name == '발걸음이_적은':
            return True
    return False


#[0]Total exp, [1]questFinishExp, [2]reviewExp, [3]alienateActivityExp
#레벨 보상 관련 로직
#레벨 1부터시작 / 3업마다 외형 변화 / 12랩이 만랩
def UpdateLevel(request, isReview, isAlienate, expInfoList):
    user = User.objects.get(id=request.user.id)
    origin_exp = user.exp

    if (isReview == True): #리뷰작성시
        user.exp = user.exp + 35
        user.save()
        expInfoList[2] += 35
    elif(isReview == False): #그냥 퀘스트완료시
        user.exp = user.exp + int(100 / (user.level / 1.5))
        user.save()
        expInfoList[1] += int(100 / (user.level / 1.5))

    if (isAlienate == True): #소외된 관광지인경우
        user.exp = user.exp + 35
        user.save()
        expInfoList[3] += 35

    elif (isAlienate == False):
        pass

    expInfoList[0] += int(expInfoList[1]+expInfoList[2]+expInfoList[3])

    if(user.exp >= 100):
        user.level += 1
        user.exp %= 100
        user.save()

    return user

#칭호 보상 관련 로직
#완료한 퀘스트 1, 3, 5, 7, 9, 12
def UpdateTitle(request):
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    # 완료된 퀘스트수 기반 칭호 부여
    DoneQuest = User_Activity.objects.filter(user_num_id=user_id, questDone=1) #유저가 완료한 퀘스트 목록
    DoneQuestNum = DoneQuest.count()

    title_nums =[]

    if DoneQuestNum == 1:
        newUserQuestTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=1)
    elif DoneQuestNum == 3:
        newUserQuestTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=2)
    elif DoneQuestNum == 5:
        newUserQuestTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=3)
    elif DoneQuestNum == 7:
        newUserQuestTitle =User_Title.objects.create(user_num_id=user_id, title_num_id=4)
    elif DoneQuestNum == 9:
        newUserQuestTitle =User_Title.objects.create(user_num_id=user_id, title_num_id=5)
    else:
        newUserQuestTitle = None

    if  newUserQuestTitle != None:
        title_nums.append(newUserQuestTitle.title_num_id)

    #후기 작성수 기반 칭호 부여
    UsersReview = Review.objects.filter(user_num_id=user_id)
    UsersReviewNum = Review.objects.filter(user_num_id=user_id).count()
    print('UsersReviewNum')
    print(UsersReviewNum)

    if UsersReviewNum == 1:
        newUserReviewTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=6)
        print('if UsersReviewNum == 1:')
    elif UsersReviewNum == 4:
        newUserReviewTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=7)
    elif UsersReviewNum == 6:
        newUserReviewTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=8)
    elif UsersReviewNum == 8:
        newUserReviewTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=9)
    elif UsersReviewNum == 10:
        newUserReviewTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=10)
    else:
        newUserReviewTitle = None

    if  newUserReviewTitle != None:
        title_nums.append(newUserReviewTitle.title_num_id)

    #레벨 기반 칭호 부여
    if user.level == 2:
        newUserlevelTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=11)
    elif user.level == 7:
        newUserlevelTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=12)
    elif user.level == 15:
        newUserlevelTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=13)
    else:
        newUserlevelTitle = None

    if newUserlevelTitle != None:
        title_nums.append(newUserlevelTitle.title_num_id)

    newTitle = Title.objects.filter(pk__in=title_nums)

    #획득한 타이틀이 다수일 경우 쿼리셋 합쳐서 반환 https://wayhome25.github.io/django/2017/11/26/merge-queryset/
    return newTitle


#레벨 보상 관련 로직
#레벨 1부터시작 / 3업마다 외형 변화 / 12랩이 만랩
def UpdateCharacter(request):
    user = User.objects.get(id=request.user.id)
    character_num = user.character_num_id

    # 레벨 기반 칭호 부여
    if user.level == 3:
        newCharacterImage = CharacterImage.objects.get(character_num_id=user.character_num_id, level =2) #유저가 보유한 케릭터의 2단계 케릭터 이미지 객체를 가져옴
        User_Character.objects.filter(user_num_id=request.user.id).update(characterImage_num_id=newCharacterImage.num)
    elif user.level == 6:
        newCharacterImage = CharacterImage.objects.get(character_num_id=user.character_num_id,level=3)  # 유저가 보유한 케릭터의 3단계 케릭터 이미지 객체를 가져옴
        User_Character.objects.filter(user_num_id=request.user.id).update(characterImage_num_id=newCharacterImage.num)
    elif user.level == 12:
        newCharacterImage = CharacterImage.objects.get(character_num_id=user.character_num_id,level=4)  # 유저가 보유한 케릭터의 4단계 케릭터 이미지 객체를 가져옴
        User_Character.objects.filter(user_num_id=request.user.id).update(characterImage_num_id=newCharacterImage.num)
    elif user.level == 15:
        newCharacterImage = CharacterImage.objects.get(character_num_id=user.character_num_id,level=5)  # 유저가 보유한 케릭터의 5단계 케릭터 이미지 객체를 가져옴
        User_Character.objects.filter(user_num_id=request.user.id).update(characterImage_num_id=newCharacterImage.num)
    else:
        newCharacterImage = None

    #케릭터 외형변화 로직추가하고 새롭게 변화된 외형 리턴해줘야함
    return newCharacterImage

#FinishQuest 기능
#1.퀘스트 완료처리
#2.레벨업 처리 -> 레벨에 따른 케릭터 변경처리
#3.칭호처리 -> 완료퀘스트수, 작성한 댓글수, 레벨 기반 칭호 부여
#4.최종적으로 UdpateUser, UdpateTitle, UdpateCharacter 3개 데이터 반환



#퀘스트 완료 처리를 해줌. 퀘스트 완료후 보상 적용이 된 유저의 정보와 새로 받은 칭호 정보 리턴(쿼리셋으로 quest_num 보내줘야함)
class FinishQuest(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        # 퀘스트 완료 처리
        quest_num = request.query_params['quest_num']  #쿼리셋으로 받은 퀘스트 번호
        quest = User_Activity.objects.filter(pk=quest_num)#get에서 filter로 바꿈
        # 유저가 보유한 퀘스트이면서 완료되지 않은 퀘스트일 경우만

        if (quest.get().user_num_id == request.user.id and quest.get().questDone == False):
            print("Dfsfdf")
            quest.update(questDone=True)

            now = datetime.datetime.now()
            now_utc = now.replace(tzinfo=timezone.utc)
            now_local = now_utc.astimezone()

            quest.update(doneTime=now_local)

            activity = Activity.objects.get(pk = quest.get().activity_num_id)

            alienateActivityExp = 0
            questFinishExp = 0
            reviewExp = 0

            expInfoList = [0, 0, 0, 0] # [0]Total exp, [1]questFinishExp, [2]reviewExp, [3]alienateActivityExp

            newUser = UpdateLevel(request, False, isAlienate(activity),expInfoList)
            newTitle= UpdateTitle(request)
            newCharacterImage = UpdateCharacter(request)


            user_serializer = UserSerializer(newUser)
            title_serializer = TitleSerializer(newTitle, many=True)
            newCharacterImage_serializer = CharacterImageSerializer(newCharacterImage)

            return Response({"UpdateUser": user_serializer.data, "NewTitle": title_serializer.data, "NewCharacterImage": newCharacterImage_serializer.data ,"TotalExp" : expInfoList[0], "QuestFinishExp":expInfoList[1], "ReviewExp":expInfoList[2],"AlienateActivityExp":expInfoList[3]})
        return Response(status=status.HTTP_400_BAD_REQUEST) #유저가 보유한 퀘스트가 아니거나 이미 완료한 퀘스트면 400리턴

#쿼리셋으로 activity_num 번호 받으면 해당하는 activity와 activity에 대한 review 데이터 제공(쿼리셋으로 activity_num 보내줘야함)
class ActivityReview(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        activity_num = request.query_params['activity_num']#엑티비티 번호
        activity = Activity.objects.get(pk=activity_num)
        activity_serializer = ActivitySerializer(activity)

        review = Review.objects.filter(activity_num_id=activity_num)
        review_serializer = ReviewSerializer(review, many=True)

        activity_preference = Activity_Preference.objects.filter(activity_num_id=activity_num)
        activity_preference_serializer = ActivityPreferenceSerializer(activity_preference, many=True)
        i=1
        return Response({"Activity" : activity_serializer.data, "Reviews" : review_serializer.data,"ActivityPreference": activity_preference_serializer.data})

#리뷰를 작성하게 해줌

#activity 평균 평점 계산 로직구현해야함
class WriteReview(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        quest = User_Activity.objects.filter(user_num_id=request.user.id, activity_num_id=request.data.get('activity_num'), questDone=1, reviewDone=0)
        isQuestExist = quest.exists()
        if isQuestExist: #사용자가 완료한 퀘스트가 존재하고 아직 리뷰를 작성하지 않았을 경우에만 리뷰작성 가능
            quest.update(reviewDone = True)
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                review = serializer.instance
                review.date = datetime.datetime.now().date()
                review.user_num_id = request.user.id

                expInfoList = [0, 0, 0, 0]

                newUser = UpdateLevel(request, True, False, expInfoList)#isReview = True, isAlienate = Fase, '발걸음이_적은' 태그 추가 경험치는 findQuest일 경우에만
                newTitle = UpdateTitle(request)
                newCharacterImage = UpdateCharacter(request)
                newCharacterImage_serializer = CharacterImageSerializer(newCharacterImage)

                user_serializer = UserSerializer(newUser)
                title_serializer = TitleSerializer(newTitle, many=True)

                #엑티비티 평점 계산 로직
                Review.objects.filter()
                avg_grade = Review.objects.filter(activity_num_id = request.data.get('activity_num')).aggregate(Avg('grade'))
                activity = Activity.objects.filter(pk=request.data.get('activity_num'))
                activity.update(grade=avg_grade['grade__avg'])

                activity_preference = Activity_Preference.objects.filter(activity_num_id=request.data.get('activity_num'))
                activity_preference_serializer = ActivityPreferenceSerializer(activity_preference, many=True)

                return Response({"UpdateUser": user_serializer.data, "NewTitle": title_serializer.data, "NewCharacterImage": newCharacterImage_serializer.data,"ActivityPreference": activity_preference_serializer.data,
                                 "TotalExp":expInfoList[0],"QuestFinishExp":expInfoList[1],"ReviewExp":expInfoList[2],"AlienateActivityExp":expInfoList[3]})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

#회원가입
class Signup(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        user_serializer = UserSerializerWithToken(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            characterImage = CharacterImage.objects.get(level=1, character_num_id=user_serializer.instance.character_num_id)
            characterImage_serializer=CharacterImageSerializer(characterImage)
            User_Character.objects.create(user_num_id=user_serializer.data['id'], characterImage_num_id=characterImage.num)

            return Response({"User": user_serializer.data, "UserCharacterImage": characterImage_serializer.data})
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#현재 유저 정보 확인
@api_view(['GET'])
def CurrentUser(request):
    user_serializer = UserSerializer(request.user)
    user_character = User_Character.objects.get(user_num_id=request.user.id)
    a=1
    characterImage = CharacterImage.objects.get(pk=user_character.characterImage_num_id)
    characterImage_serializer = CharacterImageSerializer(characterImage) #유저의 케릭터 이미지 정보 직렬화

    return Response({"User": user_serializer.data, "UserCharacterImage": characterImage_serializer.data})



#주소 업데이트
class UpdateUserAddress(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        User.objects.filter(pk=request.user.id).update(address=request.data.get('address'))
        User.objects.filter(pk=request.user.id).update(postNum=request.data.get('postNum'))
        User.objects.filter(pk=request.user.id).update(longitude=request.data.get('longitude'))
        User.objects.filter(pk=request.user.id).update(latitude=request.data.get('latitude'))
        user_serializer = UserSerializer(request.user)
        return Response({"UpdatedUser": user_serializer.data})

#칭호 업데이트
class UpdateUserTitle(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        User.objects.filter(pk=request.user.id).update(title_num_id=request.data.get('title'))
        title = Title.objects.get(pk=request.data.get('title'))
        title_serializer = TitleSerializer(title)
        return Response({"UpdatedTitle": title_serializer.data})



#선호도(태그) 업데이트
class UpdateUserPreference(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):

        tags = request.data.get('tag')
        User_Preference.objects.filter(user_num_id=request.user.id).delete()
        for tag in tags:  # 배열로 받은 태그 데이터를 하나하나 뽑음
            User_Preference.objects.create(user_num_id=request.user.id, preference_num_id=tag)

        user_tags = Preference.objects.filter(pk__in=tags)
        preference_serializer = PreferenceSerializer(user_tags, many=True)

        return Response({"UpdatedTag": preference_serializer.data})



def SortByDistance(user):
    activity_items =Activity.objects.all()
    activity_distance = round(distance.euclidean(()))
    return activity_items

def RecommendToAll(ListView):
    with transaction.atomic():
        print("로직 실행@@@@@@@@@@@@")
        User_Activity.objects.filter(questDone=0).delete()  #이전에 추천된 완료되지 않은 퀘스트 목록 삭제

        # 모든 유저에 대하여 모든 엑티비티의 자코드 유사도를 구하고 그중 상위 10개중에 3개를 추출하여 user_activity(quest)테이블에 넣어야한다.
        activity_jacard_shema = {'activity_num': [], 'jacard_similarity': [], 'distance':[]}
        activity_jacard_data = pandas.DataFrame(activity_jacard_shema)  # activity, jacard 유사도 데이터 프레임 테이블

        user_items = User.objects.all()
        for user_item in user_items: #모든 user 튜플을 가져와서 하나씩 꺼낸다.
            i = 0
            user_id = user_item.id
            User_Preference_items = User_Preference.objects.filter(user_num_id=user_id)  #각 user들이 가지고 있는 preference 목록
            user_tags = []  #자카드 유사도를 구하기 위해 딕셔너리 형태로 preference를 정리해 놓음, 유저의 preference 목록임(preference의 name에 띄어쓰기가 있으면 안된다.)
            #ex) ['분위기있는' '야외의' '실내의' '신나는']
            for User_Preference_item in User_Preference_items:
                tag = Preference.objects.get(pk=User_Preference_item.preference_num_id)#user_preference 튜플의(item) preference 키를 이용하여 prefernce 튜플을 추출한후 preference의 이름을 tag에 저장
                user_tags.append(tag.name)  # 유저가 보유한 태그 딕셔너리에 preferene를 추가

            activity_items = Activity.objects.all()  # 모든 엑티비티를 가져와서
            for activity_item in activity_items:  # 하나씩 엑티비티의 태그와 유저의 태그에 대해 자카드 유사도를 계산한다.
                activity_tags = []
                items = Activity_Preference.objects.filter(activity_num_id=activity_item.num)  # 엑티비티가 가지고 있는 선호도 목록
                for item in items:
                    tag = Preference.objects.get(pk=item.preference_num_id)
                    activity_tags.append(tag.name)  # 엑티비티가 보유한 태그 딕셔너리
                union = set(user_tags).union(set(activity_tags))  # 합집합
                intersection = set(user_tags).intersection(set(activity_tags))  # 교집합합
                try:#태그가 없을 경우 len이 0이 되어 ZeroDivision 오류나서 예외처리해줌
                    jacard_similarity = len(intersection) / len(union)  # 유저태그와 엑티비티태그의 자카드 유사도
                except(ZeroDivisionError):
                    jacard_similarity=0

                distanceFromUser = round(distance.euclidean((activity_item.longitude, activity_item.latitude),(user_item.longitude,user_item.latitude)),5)

                #print("유저거리")
                #print(distanceFromUser)
                #print()
                # 엑티비티, 자카드 유사도
                activity_jacard_data.loc[i] = [activity_item.num, jacard_similarity, distanceFromUser]  # 엑티비티 번호, 자카드 유사도 insert
                i += 1
            print("자카드 유사도")
            print(activity_jacard_data)
            print()

            # 이미 유저가 완료한 퀘스트에 해당하는 엑티비티 제거 로직
            quest_items = User_Activity.objects.filter(user_num_id = user_id)
            print(user_id)
            print("번 유저의 퀘스트")
            for item in quest_items:
                print(item.questDone)
                if(item.questDone == True):
                    print(item.questDone)
                    print(item.activity_num_id)
                    print("깡ㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇ")
                    print("삭제이후")
                    activity_jacard_data = activity_jacard_data[activity_jacard_data.activity_num != item.activity_num_id]
                    print(activity_jacard_data)
                    print()


            activity_jacard_data_sorted = activity_jacard_data.sort_values(by=['jacard_similarity', 'distance'], ascending=[False, True])  # 유저태그와 엑티비티태그에 대한 자카드유사도 계산후 오름차순정렬
            activity_jacard_data_sorted_10 = activity_jacard_data_sorted.head(15)  # 자카드 유사도순 상위 50개의 데이터프레임 추출
            activity_jacard_data_sorted_3 = activity_jacard_data_sorted_10.sample(n=3)  # 자카드 유사도순 상위 10개의 데이터프레임중 랜덤으로 3개의 데이터프레임 추출
            activity_jacard_data_sorted_3 = activity_jacard_data_sorted_3.reset_index(drop=True)  # 인덱스 0부터 시작하도록 초기화
            activity_jacard_data_sorted_3 = activity_jacard_data_sorted_3['activity_num']  # 엑티비티 속성만 추출

            print(user_id)
            print("번 유저에 대한 추천 데이터 10개")
            pprint.pprint(activity_jacard_data_sorted_10)
            print()

            print(user_id)
            print("번 유저에 대한 추천 데이터 3개")
            print(activity_jacard_data_sorted_3)
            print("포문 시작")
            for i in range(3):
                print("User_activity 인스턴스 생성")
                quest = User_Activity.objects.create(user_num_id=user_id, activity_num_id=activity_jacard_data_sorted_3.iloc[i]).save()
    return 0

def AllQuestAllocation(request):
    RecommendToAll(request)
    return render(request, 'test.html', {})

@api_view(['GET'])
def QuestAllocation(request):
    with transaction.atomic():
        print("로직 실행@@@@@@@@@@@@")
        activity_jacard_shema = {'activity_num': [], 'jacard_similarity': [], 'distance':[]}
        activity_jacard_data = pandas.DataFrame(activity_jacard_shema)  # activity, jacard 유사도 데이터 프레임 테이블

        user_item = User.objects.get(pk=request.user.id)
        i=0
        user_id = user_item.id
        User_Preference_items = User_Preference.objects.filter(user_num_id=user_id)  #각 user들이 가지고 있는 preference 목록
        user_tags = []  #자카드 유사도를 구하기 위해 딕셔너리 형태로 preference를 정리해 놓음, 유저의 preference 목록임(preference의 name에 띄어쓰기가 있으면 안된다.)
        #ex) ['분위기있는' '야외의' '실내의' '신나는']
        for User_Preference_item in User_Preference_items:
            tag = Preference.objects.get(pk=User_Preference_item.preference_num_id)#user_preference 튜플의(item) preference 키를 이용하여 prefernce 튜플을 추출한후 preference의 이름을 tag에 저장
            user_tags.append(tag.name)  # 유저가 보유한 태그 딕셔너리에 preferene를 추가
        activity_items = Activity.objects.all()  # 모든 엑티비티를 가져와서

        for activity_item in activity_items:  # 하나씩 엑티비티의 태그와 유저의 태그에 대해 자카드 유사도를 계산한다.
            activity_tags = []
            items = Activity_Preference.objects.filter(activity_num_id=activity_item.num)  # 엑티비티가 가지고 있는 선호도 목록
            for item in items:
                tag = Preference.objects.get(pk=item.preference_num_id)
                activity_tags.append(tag.name)  # 엑티비티가 보유한 태그 딕셔너리
            union = set(user_tags).union(set(activity_tags))  # 합집합
            intersection = set(user_tags).intersection(set(activity_tags))  # 교집합합
            try:#태그가 없을 경우 len이 0이 되어 ZeroDivision 오류나서 예외처리해줌
                jacard_similarity = len(intersection) / len(union)  # 유저태그와 엑티비티태그의 자카드 유사도
            except(ZeroDivisionError):
                jacard_similarity=0
            # 엑티비티, 자카드 유사도

            distanceFromUser = round(distance.euclidean((activity_item.longitude, activity_item.latitude),(user_item.longitude, user_item.latitude)), 5)
            activity_jacard_data.loc[i] = [activity_item.num, jacard_similarity,distanceFromUser]  # 엑티비티 번호, 자카드 유사도 insert
            i += 1

        # 이미 유저가 완료한 퀘스트에 해당하는 엑티비티 제거 로직
        quest_items = User_Activity.objects.filter(user_num_id=request.user.id)
        print("번 유저의 퀘스트")
        for item in quest_items:
            print(item.questDone)
            if (item.questDone == True):
                print(item.questDone)
                print(item.activity_num_id)
                print("깡ㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇ")
                print("삭제이후")
                activity_jacard_data = activity_jacard_data[activity_jacard_data.activity_num != item.activity_num_id]
                print(activity_jacard_data)
                print()

        print("자카드 유사도")
        print(activity_jacard_data)

        activity_jacard_data_sorted = activity_jacard_data.sort_values(by=['jacard_similarity', 'distance'], ascending=[False, True])  # 유저태그와 엑티비티태그에 대한 자카드유사도 계산후 오름차순정렬
        activity_jacard_data_sorted_10 = activity_jacard_data_sorted.head(15)  # 자카드 유사도순 상위 50개의 데이터프레임 추출
        activity_jacard_data_sorted_3 = activity_jacard_data_sorted_10.sample(n=3)  # 자카드 유사도순 상위 10개의 데이터프레임중 랜덤으로 3개의 데이터프레임 추출
        activity_jacard_data_sorted_3 = activity_jacard_data_sorted_3.reset_index(drop=True)  # 인덱스 0부터 시작하도록 초기화
        activity_jacard_data_sorted_3 = activity_jacard_data_sorted_3['activity_num']  # 엑티비티 속성만 추출
        print(user_id)
        print("번 유저에 대한 추천 데이터 3개")
        print(activity_jacard_data_sorted_3)
        print("포문 시작")
        for i in range(3):
            print("User_activity 인스턴스 생성")
            quest = User_Activity.objects.create(user_num_id=user_id, activity_num_id=activity_jacard_data_sorted_3.iloc[i]).save()
    return Response(status=status.HTTP_201_CREATED)



