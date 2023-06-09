from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('insights/dashboard', views.dashboard, name="dashboard"),
]