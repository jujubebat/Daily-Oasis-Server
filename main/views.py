from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken, ActivitySerializer
from .models import Activity, User_Preference, Preference, Activity_Preference, User_Activity, Title, User
import pandas

#데이터베이스로부터 데이터를 가져오고, 선언해둔 시리얼라이저를 통해 데이터를 직렬화해준다.
class activity(APIView):
    def Jaccard_similarity(self):
        return list

    def get_object(self):
        return Activity.objects.all()

    def get(self, request):
        jacard_data = {'activity_num':[],'Jacard_similarity':[]}
        activity_jacard = pandas.DataFrame(jacard_data) #activity, jacard 유사도 테이블
        i=0
        user_id = request.user.id
        items = User_Preference.objects.filter(user_num_id=user_id)#유저가 가지고 있는 선호도 목록
        user_tags=[] #유저의 태그(선호)목록(태그에 띄어쓰기가 있으면 안된다.)
        for item in items:
            tag=Preference.objects.get(pk=item.preference_num_id)
            user_tags.append(tag.name) #유저가 보유한 태그 딕셔너리

        activity_items = Activity.objects.all()#모든 엑티비티를 가져와서
        for activity_item in activity_items:#하나씩 엑티비티의 태그와 유저의 태그에 대해 자카드 유사도를 계산한다.
            activity_tags = []
            items = Activity_Preference.objects.filter(activity_num_id=activity_item.num)#엑티비티가 가지고 있는 선호도 목록
            for item in items:
                tag = Preference.objects.get(pk=item.preference_num_id)
                activity_tags.append(tag.name) #엑티비티가 보유한 태그 딕셔너리

            union = set(user_tags).union(set(activity_tags)) #합집합
            intersection = set(user_tags).intersection(set(activity_tags)) #교집합합
            Jacard_similarity = len(intersection)/len(union) #유저태그와 엑티비티태그의 자카드 유사도
            #엑티비티, 자카드 유사도
            activity_jacard.loc[i]=[activity_item.num,Jacard_similarity] #엑티비티 번호, 자카드 유사도 insert
            i+=1

        activity_jacard=activity_jacard.sort_values(by=['Jacard_similarity'], ascending=False)#유저태그와 엑티비티태그에 대한 자카드유사도 계산후 오름차순정렬
        #print(activity_jacard)

        activity_jacard_10=activity_jacard.head(10) #자카드 유사도순 상위 10개의 데이터프레임 추출
        activity_jacard_3 = activity_jacard_10.sample(n=3) #자카드 유사도순 상위 10개의 데이터프레임중 3개의 데이터프레임 추출
        activity_jacard_3=activity_jacard_3.reset_index(drop=True)#인덱스 0부터 시작하도록 초기화
        activity_jacard_3 = activity_jacard_3['activity_num']#엑티비티 속성만 추출
        data = Activity.objects.filter(pk__in=[activity_jacard_3.iloc[0], activity_jacard_3.iloc[1], activity_jacard_3.iloc[2]])# 3개의 엑티비티 데이터를 뽑아낸다.

        serializer = ActivitySerializer(data, many=True) #many 옵션은 여러 객체를 직렬화 해준다.

        #퀘스트 할당하는 로직짜야함.
        #그리고 완료된 퀘스트 반환하는 로직짜야함.
        #자코드 알고리즘으로 3개 추천 -> 모든 유저에 대해서 12시마다 새로운 엑티비티 추천해주는것 view로 구현하고 crontab로 돌려야함
        #위코드를 하나의 view로 구현하면됨 12시가 되면 user_activity 싹지우고 새로운 3개의 엑티비티 할당
        #api로 구현해야할 것은 user_activity 테이블에서 데이터 뽑아서 주는 것 밖에 없음
        data2 = Activity.objects.get(pk=1)
        serializer2 = ActivitySerializer(data2)
        return Response({"CurrentQuest":serializer2.data})

@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def scheduler():
    #기존 데이터 초기화
    # data = User_Activity.objects.all()
    # data.delete()

    temp = Title.objects.create()
    temp.name = 'hello world'
    temp.save()

    # #모든 유저에 대한 모든 엑티비티의 자코드 유사도를 구하고 그중 상위 10개중에 3개를 추출하여 user_activity(quest)테이블에 넣어야한다.
    activity_jacard_shema = {'activity_num': [], 'Jacard_similarity': []}
    activity_jacard_data = pandas.DataFrame(activity_jacard_shema)  # activity, jacard 유사도 데이터 프레임 테이블
    i = 0

    user_items = User.objects.all()

    for user_item in user_items: #모든 user 튜플을 가져와서 하나씩 꺼낸다.
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
            Jacard_similarity = len(intersection) / len(union)  # 유저태그와 엑티비티태그의 자카드 유사도
            # 엑티비티, 자카드 유사도
            activity_jacard_data.loc[i] = [activity_item.num, Jacard_similarity]  # 엑티비티 번호, 자카드 유사도 insert
            i += 1

        activity_jacard_data_sorted = activity_jacard_data.sort_values(by=['Jacard_similarity'],ascending=False)  # 유저태그와 엑티비티태그에 대한 자카드유사도 계산후 오름차순정렬
        activity_jacard_data_sorted_10 = activity_jacard_data_sorted.head(10)  # 자카드 유사도순 상위 10개의 데이터프레임 추출
        activity_jacard_data_sorted_3 = activity_jacard_data_sorted_10.sample(n=3)  # 자카드 유사도순 상위 10개의 데이터프레임중 랜덤으로 3개의 데이터프레임 추출
        activity_jacard_data_sorted_3 = activity_jacard_data_sorted_3.reset_index(drop=True)  # 인덱스 0부터 시작하도록 초기화
        activity_jacard_data_sorted_3 = activity_jacard_data_sorted_3['activity_num']  # 엑티비티 속성만 추출

        for i in range(3):
            quest = User_Activity.objects.create()
            quest.user_num = User.objects.get(pk=user_id)
            quest.activity_num = Activity.objects.get(pk=activity_jacard_data_sorted_3.iloc[i])
    return 0