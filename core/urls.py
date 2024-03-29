from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.signup, name="signup"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('insights/dashboard', views.dashboard, name="dashboard"),
] + static(settings.STATIC_URL)