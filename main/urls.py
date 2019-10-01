from django.conf import settings
from django.urls import path
from django.conf.urls import include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view
from . import views
from .views import Signup

urlpatterns = [
    path('silk', include('silk.urls', namespace='silk')),
    path('allQuestAllocation', views.AllQuestAllocation), #모든 유저에게 새로운 퀘스트 할당
    path('questAllocation', views.QuestAllocation), #한 명의 유저에게 새로운 퀘스트 할당
    #[개발완료]
    #토큰 필요
    path('signup', Signup.as_view()), #검수완료/ 회원가입
    path('writeReview', views.WriteReview.as_view()),  # 검수완료/ 리뷰작성로직 실행
    path('currentQuest', views.CurrentQuest.as_view()),  # 검수완료 / 유저가 진행중인 퀘스트 데이터 제공(엑티비티 제공)
    path('doneQuest', views.DoneQuest.as_view()),  # 검수완료 / 유저가 완료한 퀘스트 제공(발자취)
    path('currentUser', views.CurrentUser), #검수완료 / 정보 데이터 제공
    path('finishQuest', views.FinishQuest.as_view()), #검수완료 /퀘스트 완료 로직 실행 후 갱신된 유저 정보와 새로얻은 칭호 정보제공 (두 개의 모델을 하나로 직렬화) /finishQuest?activity_num=1
    path('activityReview', views.ActivityReview.as_view()), #검수완료/ 엑티비티와 엑티비티에 달려있는 댓글 데이터 제공 (두 개의 모델을 하나로 직렬화) /activityReview?activity_num=1
    #토큰 필요없음
    path('login', obtain_jwt_token), #검수완료 / 로그인
    path('activityList', views.ActivityList.as_view()), #검수완료 / 모든 엑티비티 데이터 제공
    #개발중
    path('updateUser', views.UpdateUserNickName.as_view()),
    path('updatePreference', views.UpdateUserPreference.as_view()),
    path('updateAddress', views.UpdateUserAddress.as_view()),
    path('updateCharacter', views.UpdateUserCharacter.as_view()),
    #path('characterList',views.CharacterList.as_view()),
    #path('titleList', views.TitleList.as_view()),
]

#API 자동화 문서 라이브러리 관련(django swagger)
schema_view = get_swagger_view(title='Pastebin API')
urlpatterns += [
    path('apiDocument', schema_view)
]

# #디버그 툴 관련
# if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
#     import debug_toolbar
#     urlpatterns += [
#         path('debug/', include(debug_toolbar.urls)),
#     ]

'''
<업데이트 예정(우선 순위순)>
-tmap 지오코딩 활용하여 근거리 추천 기능 추가(핵심) 
-crontab 잘 작동하는지 테스트 
-퀘스트 완료시 '소외된' 태그가 있는 엑티비티일 경우 추가 경험치 부여 
-유저 업데이트 기능 구현(승륜이랑 얘기하면서 구현)
-중복 추천 허용 안하는 기능 추가 
-utils.py에 시리얼라이져 등록 
-회원가입시 이메일 인증 기능 구현 
-모든 케릭터 정보 제공하는 api 구현
'''

'''
<업데이트 진행중>
/current_user -> /currentUser
'''

'''
<업데이트 완료 사항(AWS반영 완료)>
-디비 초기화->샘플 데이터 넣는 작업 필요
-signup : 케릭터 이미지 정보 제공(엑티비티, 리뷰 제공 안되게 수정)
-current_user : 케릭터 이미지 정보 제공
-레벨에 따른 케릭터 변화 로직 추가
-finishQuest, writeReview에서 UpdateUser,NewTitle,NewCharacterImage 데이터 제공 
-writeReview시 고정 경험치 25 제공 
-Activity 평점 계산로직 추가(writeReview로 테스트 바람)
- /allQuestAllocation : 모든 유저의 퀘스트 업데이트 
- /questAllocation : 유저 한명의 퀘스트 업데이트 api(회원가입시 활용 바람) request로 token 보내줘야함
- UTC시간 한국시간으로 변경 / 리뷰작성 시간 속성명 변경 date -> doneTime(finishQeust와 통일)
- /api_doc 이름수정 -> /apiDocument
'''

'''
프로젝트가 끝난후
포트폴리오를 위한 장고, 파이썬, 웹에 대해 공부하고 정리해야할것들
-프로젝트 명세서 간략하게 작성(기술적으로, 서비스적으로 나눠서 작성)
-JWT 어떤식으로 구현되는지 공부
-파이썬 문법공부
-Rest 정의 공부
-시리얼라이저 공부
-json에 대한 공부 (xml과의 차이점 공부)
-장고 orm에 대해 정리
-GET과 POST에 대해 정리
-서버 응당 404,400,200 등등에 대한 대략적인 의미파악하기
'''




