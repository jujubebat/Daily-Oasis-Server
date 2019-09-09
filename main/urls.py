from django.urls import path
from .views import current_user, UserList, activity
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('current_user/', current_user),
    path('signup/', UserList.as_view()),
    path('activity/', views.activity.as_view()),
    path('login/', obtain_jwt_token),
]