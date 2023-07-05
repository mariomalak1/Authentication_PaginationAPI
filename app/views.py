from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from .serializers import Registration_Serializer, Login_Serializer, User_Serializer
from .permissions import is_authenticated_user
# Create your views here.


@api_view(["POST"])
def login(request):
	data = request.data
	serializer = Login_Serializer(data=data)
	if serializer.is_valid():
		user = authenticate(username=serializer.data.get("username"), password=serializer.data.get("password"))
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

@api_view(["GET", "PUT", "Delete"])
@is_authenticated_user
def user_(request, user_obj):
	if request == "GET":
		pass
