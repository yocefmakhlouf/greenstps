"""dash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import LDAPLogin,register,gets_steps,GetUsers,GetData,GetuData,GetmData,send,setevent,getevent,geteventdata,connect,logout,getuserchat,GetmDatau,GetInfo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',LDAPLogin.as_view()),
    path('register/',register.as_view()),
    path('api/getsteps/',gets_steps.as_view()),
    path('api/getusers/',GetUsers.as_view()),
    path('api/getdata/',GetData.as_view()),
    path('api/getudata/',GetuData.as_view()),
    path('api/getmdata/',GetmData.as_view()),
    path('api/send/',send.as_view()),
    path('api/setevent/',setevent.as_view()),
    path('api/getevent/',getevent.as_view()),
    path('api/geteventdata/',geteventdata.as_view()),
    path('api/connect/',connect.as_view()),
    path('api/logout/',logout.as_view()),
    path('api/chats/',getuserchat.as_view()),
    path('api/user/getmdata/',GetmDatau.as_view()),
    path('api/user/getinfo/',GetInfo.as_view()),

]
