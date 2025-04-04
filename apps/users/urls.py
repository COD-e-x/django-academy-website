from django.urls import path

from .apps import UsersConfig
from . import views


app_name = UsersConfig.name


urlpatterns = [
    path("", views.user_login, name="login"),
    path("register/", views.user_register, name="register"),
    path("profile/", views.user_profile, name="profile"),
    path("logout/", views.user_logout, name="logout"),
]
