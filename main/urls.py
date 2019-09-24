from django.conf import settings
from django.urls import path
from django.conf.urls import include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view
from . import views
from .views import  DoneQuest, ActivityList, CurrentQuest, FinishQuest, UserList, #ActivityReview

urlpatterns = [
    path('current_user', views.current_user),
    path('silk', include('silk.urls', namespace='silk')),
    path('test',views.test),
    path('login', obtain_jwt_token),
    path('signup', UserList.as_view()),
    path('activityList', views.ActivityList),
    path('currentQuest', views.DoneQuest),
    path('doneQuest', views.CurrentQuest),
    path('finishQuest', views.FinishQuest),
    #path('activityReview', ActivityReview.as_view()), #엑티비티하고 엑티비티 리뷰들 제공
    path('writeReview', views.WriteReview),  #리뷰작성
]

#퀘스트 완료 -> 레벨, 칭호 로직 반영
#댓글 기능 -> 레벨, 칭호, 로직 반영

#디버그 툴 관련
if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        path('debug/', include(debug_toolbar.urls)),
    ]

#API 자동화 문서 라이브러리 관련(django swagger)
schema_view = get_swagger_view(title='Pastebin API')
urlpatterns += [
    path('api_doc', schema_view)
]

#DoneQuest 엑티비티를 넘겨줄지 아님 엑티비티 pk를 넘겨줄지 정해야함
#메모
#위치기반 추천기능 추가
#Tmap 지오코딩
#만들어야할 api 목록




