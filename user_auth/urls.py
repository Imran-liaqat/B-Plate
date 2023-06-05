from rest_framework.authtoken import views
from django.contrib import admin
from django.urls import path , include
from APP.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token),
    path('auth/user/signup/',UserSignup.as_view()),
    path('auth/Phone_exit/signup/',CheckUsername.as_view()),
    path('auth/User/forgot-password/',ForgotPassword.as_view()),
    path('auth/User/Rset-Password/',ResetPassword.as_view())
    
]
