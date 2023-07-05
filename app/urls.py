from django.urls import path
from .views import *
urlpatterns = [
	path("users/", users, name="users"),
	path("user/", user_, name="user"),
	path("login/", login, name="login"),
]