from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("community/", views.community, name="community"),
    path("dreams/", views.dreams, name="dreams"),
    path("dreams/new/", views.dream_new, name="dream_new"),
    path("dreams/<int:pk>/", views.dream_detail, name="dream_detail"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
]
