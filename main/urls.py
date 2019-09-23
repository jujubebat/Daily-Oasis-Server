from django.conf import settings
from django.urls import path
from django.conf.urls import include, url
from .views import current_user, UserList, activity, CurrentQuest
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('current_user/', current_user),
    path('silk/', include('silk.urls', namespace='silk')),
    path('test/',views.test),
    path('login/', obtain_jwt_token),
    path('signup/', UserList.as_view()),
    path('currentQuest/', CurrentQuest.as_view()),
    #path('doneQuest/', CurrentQuest.as_view()),
    path('activity/', activity.as_view()),
]

# if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
#     import debug_toolbar
#     urlpatterns += [
#         path('debug/', include(debug_toolbar.urls)),
#     ]
#







