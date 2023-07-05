from django.urls import path
from .views import *
urlpatterns = [
	path("users/", users, name="users"),
	path("login/", login, name="login"),
]