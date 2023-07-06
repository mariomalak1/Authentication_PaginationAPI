import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login as django_login_user, logout as django_logout_user 
from django.contrib.auth.models import User
from django.core.paginator import Paginator	
from django.shortcuts import get_object_or_404
from .serializers import Registration_Serializer, Login_Serializer, User_Serializer
from .permissions import is_authenticated_user
# Create your views here.


@api_view(["GET"])
def login(request):
	data = request.data
	serializer = Login_Serializer(data=data)
	if serializer.is_valid():
		user = authenticate(username=serializer.data.get("username"), password=serializer.data.get("password"))
		django_login_user(request, user)
		if user:
			token = Token.objects.filter(user__username=user.username).first()
			if not token:
				token = Token.objects.create(user=user)
				return Response({"token":str(token)}, status=status.HTTP_200_OK)
			else:
				return Response({"token":str(token)}, status=status.HTTP_200_OK)

		else:
			return Response({"error":"Invalid Username or Password"}, status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "POST"])
def users(request):
	if request.method == "POST":
		data = request.data
		serializer = Registration_Serializer(data=data)
		if serializer.is_valid():
			user = User.objects.create(username=serializer.data.get("username"))
			user.set_password(serializer.data.get("password"))
			if serializer.data.get("email"):
				user.email = serializer.data.get("email")
			user.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == "GET":
		per_page = 2
		users_objects = User.objects.all()
		required_page = request.GET.get("page", 1)
		paginator = Paginator(users_objects, per_page)
		try:
			if int(required_page) > paginator.num_pages:
				objects_per_page = paginator.page(paginator.num_pages)
			elif int(required_page) < 1:
				objects_per_page = paginator.page(1)
			else:
				objects_per_page = paginator.page(int(required_page))
		except:
			return Response({"page error": "Enter Valid Page Number"})
		serializer = User_Serializer(objects_per_page, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@is_authenticated_user
def logout(request, user_obj):
	token = Token.objects.filter(user=user_obj).first()
	django_logout_user(request)
	token.delete()
	return Response(status=status.HTTP_200_OK)


@api_view(["GET", "PATCH", "Delete"])
@is_authenticated_user
def user_(request, user_obj):
	if request.method == "GET":
		serializer = User_Serializer(user_obj)
		return Response(serializer.data, status=status.HTTP_200_OK)

	elif request.method == "PATCH":
		data = request.data
		serializer = serializer = User_Serializer(instance=user_obj, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# helpful function to user_delete function
def delete_user_if_not_himself(user_obj, delete_user):
	if user_obj != delete_user:
		delete_user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
	else:
		return Response({"error":"You can't Delete yourself"},status=status.HTTP_403_FORBIDDEN)	


# if he is superuser he can delete any user, except himself
# if he is staff he can delete any user, but not staff user also, or himself
@api_view(["DELETE"])
@is_authenticated_user
def user_delete(request, user_obj):
	if request.method == "DELETE":
		delete_user = get_object_or_404(User, username=request.data.get('delete_username'))
		if user_obj.is_superuser:
			return delete_user_if_not_himself(user_obj, delete_user)
		elif user_obj.is_staff and (not delete_user.is_staff) and (not delete_user.is_superuser):
			return delete_user_if_not_himself(user_obj, delete_user)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)
