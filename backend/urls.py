from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from main import views

urlpatterns = [
    # path('login/', obtain_jwt_token),
    path('', include('main.urls')),
    # path('signup/', obtain_jwt_token),
    # path('login/', obtain_jwt_token),
    # path('login/', obtain_jwt_token),
]
