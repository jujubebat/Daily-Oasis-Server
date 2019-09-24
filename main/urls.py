from django.conf import settings
from django.urls import path
from django.conf.urls import include, url
from .views import current_user, UserList, ActivityList, CurrentQuest,DoneQuest,FinishQuest
from . import views
from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('current_user', current_user),
    path('silk', include('silk.urls', namespace='silk')),
    path('test',views.test),
    path('login', obtain_jwt_token),
    path('signup', UserList.as_view()),
    path('activityList', ActivityList.as_view()),
    path('currentQuest', DoneQuest.as_view()),
    path('doneQuest', CurrentQuest.as_view()),
    path('finishQuest', FinishQuest.as_view()),


]

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        path('debug/', include(debug_toolbar.urls)),
    ]
schema_view = get_swagger_view(title='Pastebin API')
urlpatterns += [
    path('api_doc', schema_view)
]


#DoneQuest 엑티비티를 넘겨줄지 아님 엑티비티 pk를 넘겨줄지 정해야함

#메모
#위치기반 추천기능 추가
#Tmap 지오코딩
#만들어야할 api 목록
#퀘스트 완료 -> 레벨, 칭호 로직 반영
#댓글 기능 -> 레벨, 칭호, 로직 반영




