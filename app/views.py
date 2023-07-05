from rest_framework.decorators import api_view
from rest_framework.response import Response 
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .serializers import Registration_Serializer, Login_Serializer
# Create your views here.

@api_view(["POST"])
def registration(request):
	data = request.data
	serializer = Registration_Serializer(data=data)
	if serializer.is_valid():
		user = User.objects.create(username=serializer.data.get("username"))
		user.set_password(serializer.data.get("password"))
		if serializer.data.get("email"):
			user.email = serializer.data.get("email")
		user.save()
		return Response(serializer.data, status=200)
	else:
		return Response(serializer.errors, status=400)

@api_view(["POST"])
def login(request):
	data = request.data
	serializer = Login_Serializer(data=data)
	if serializer.is_valid():
		user = authenticate(username=serializer.data.get("username"), password=serializer.data.get("password"))
		if user:
			return Response(serializer.data, status=200)
		else:
			return Response({"error":"Invalid Username or Password"}, status=400)
	else:
		return Response(serializer.errors, status=400)