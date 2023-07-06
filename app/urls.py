from django.urls import path
from .views import *
urlpatterns = [
	path("users/", users, name="users"),
	path("user/", user_, name="user"),
	path("user_delete/", user_delete, name="delete_user"),
	path("login/", login, name="login"),
	path("logout/", logout, name="logout"),
]