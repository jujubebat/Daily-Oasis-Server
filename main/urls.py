from django.conf import settings
from django.urls import path
from django.conf.urls import include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view
from . import views
from .views import UserList

urlpatterns = [

    path('silk', include('silk.urls', namespace='silk')),
    path('test', views.test),

    #완성된것들
    path('login', obtain_jwt_token), #로그인
    path('signup', UserList.as_view()), #회원가입
    path('current_user', views.current_user), #유저 정보 데이터 제공
    path('activityList', views.ActivityList.as_view()), #모든 엑티비티 데이터 제공
    path('activityReview', views.ActivityReview.as_view()), #엑티비티와 엑티비티에 달려있는 댓글 데이터 제공 (두 개의 모델을 하나로 직렬화) /activityReview?activity_num=1
    path('writeReview', views.WriteReview.as_view()), #리뷰작성로직 실행
    path('currentQuest', views.CurrentQuest.as_view()), #유저가 진행중인 퀘스트 데이터 제공(엑티비티 제공)
    path('doneQuest', views.DoneQuest.as_view()), #유저가 완료한 퀘스트 제공(발자취)

    path('finishQuest', views.FinishQuest.as_view()), #퀘스트 완료 로직 실행 후 갱신된 유저 정보와 새로얻은 칭호 정보제공 (두 개의 모델을 하나로 직렬화) /finishQuest?activity_num=1
    #개발예정
    # path('updateUser'), #유저 정보 수정
    # path('updatePreference'), #태그 정보 수정
]

# #디버그 툴 관련
# if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
#     import debug_toolbar
#     urlpatterns += [
#         path('debug/', include(debug_toolbar.urls)),
#     ]

#API 자동화 문서 라이브러리 관련(django swagger)
schema_view = get_swagger_view(title='Pastebin API')
urlpatterns += [
    path('api_doc', schema_view)
]

#2019-09-25 새벽 2시
'''
0. doneQuest 테스트 하자 

1.activityReview : 엑티비티의 리뷰들 제공 -> 엑티비티 pk를 받아서 엑티비티 모델과 댓글 모델 이 두 개의 모델을 한 번에 json으로 보내는 거 되는지 테스트 해야함

2.레벨업, 칭호 디비에 데이터 셋 넣어서 테스트

3.관광 3개 추천 로직 잘 돌아가는지 다시 한 번 테스트

4.utils.py에 시리얼라이져 등록 

5.writeReview 작성 로직 구현 해야함
-user pk와 activity pk, 그리고 댓글 내용을 request로 받음
-review 테이블에 리뷰추가함
-user_activity 테이블에 review썻다고 표시해야함 
-리뷰작성 경험치 줘야함(level up Udapte 로직 돌려야함->기존꺼말고 하나 더 만들어야할 수도)
-유저 정보 보내줘야함

6. tmap 지오코딩 사용해서 근거리 추천 기능 추가해야함
'''



