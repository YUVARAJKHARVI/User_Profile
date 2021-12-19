from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('Login/',views.Login, name="login"),
    path('User_profile/',views.Dashboard, name="Dashboard"),
    path('password-reset/',views.forgot_password, name="password_reset"),
    path('signout/',views.signout, name="signout"),



]
