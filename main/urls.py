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

    #토큰 필요
    path('signup', Signup.as_view()), #검수완료/ 회원가입
    path('writeReview', views.WriteReview.as_view()),  # 검수완료/ 리뷰작성로직 실행
    path('currentQuest', views.CurrentQuest.as_view()),  # 검수완료 / 유저가 진행중인 퀘스트 데이터 제공(엑티비티 제공)
    path('doneQuest', views.DoneQuest.as_view()),  # 검수완료 / 유저가 완료한 퀘스트 제공(발자취)
    path('currentUser', views.CurrentUser), #검수완료 / 정보 데이터 제공
    path('finishQuest', views.FinishQuest.as_view()), #검수완료 /퀘스트 완료 로직 실행 후 갱신된 유저 정보와 새로얻은 칭호 정보제공 /finishQuest?activity_num=1
    path('activityReview', views.ActivityReview.as_view()), #검수완료/ 엑티비티와 엑티비티에 달려있는 댓글 데이터 제공 (두 개의 모델을 하나로 직렬화) /activityReview?activity_num=1
    path('userTitleList', views.UserTitle.as_view()), #검수완료 유저의 칭호목록
    path('userPreferenceList', views.UserPreference.as_view()), #검수완료 유저의 칭호목록
    path('updateUserAddress', views.UpdateUserAddress.as_view()), #유저의 주소 업데이트
    path('updateUserTitle', views.UpdateUserTitle.as_view()), #유저의 대표칭호 업데이트
    path('updateUserPreference', views.UpdateUserPreference.as_view()), #유저의 태그 업데이트
    #토큰 필요없음
    path('login', obtain_jwt_token), #검수완료 / 로그인
    path('activityList', views.ActivityList.as_view()), #검수완료 / 모든 엑티비티 데이터 제공
    path('characterList',views.CharacterList.as_view()), #전체 케릭터정보(케릭터이미지정보포함)제공
    path('titleList', views.TitleList.as_view()), #전체 칭호 데이터 제공
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
-crontab 잘 작동하는지 테스트 (오전 10시도 설정해둠)

번외)
-회원가입시 이메일 인증 기능 구현 
'''

'''
<업데이트 진행중(AWS반영 미완료)>

'''

'''
<업데이트 완료 사항(AWS반영 완료)>
-유저 업데이트 기능 구현 / updateUserTitle 구현 : title pk 보내주면 대표칭호로 설정해주는 api 그리고 title 데이터 리턴
-currentQeust, DoneQuest, activityReview api에서 엑티비티 태그목록 반환(https://stackoverflow.com/questions/52295480/serializing-many-to-many-intermediate-table-in-django-rest-framework)
- /current_user -> /currentUser
- Activity mapx, mapy 속성 User와 통일
- /allQuestAllocation, /questAllocation : 근거리순으로 추천하는 기능 추가 / 이전에 완료한 퀘스트 추천하지 않는 기능 추가
- /finishQest : '발걸음이_적은' 태그가 달려있을 경우 exp +25 추가로 적용 
- 새로운 api characterList/ : 모든 케릭터 정보 제공
- 새로운 api titleList/ : 모든 칭호 정보제공
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
-/finishQuest, /writeReview 시 획득 exp 정보 반환 : Total exp(총획득량), questFinishExp(퀘스트완료 경험치), reviewExp(리뷰작성경험치), alienateActivityExp(소외관광지 추가 경험치)
-만렙 15로 조정 그에따른 경험치 부여 조정 : 소외된 관광지 방문시 exp 25 -> 35 상향, 리뷰 ex24->35 상향 / 15렙 달성시 만렙칭호 부여
'''

'''
<프로젝트가 끝난후 할것들>
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




