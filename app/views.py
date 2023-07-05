from rest_framework.decorators import api_view
from rest_framework.response import Response 
from django.contrib.auth.models import User

from .serializers import Login_Serializer
# Create your views here.

@api_view(["POST"])
def registration(request):
	data = request.data
	serializer = Login_Serializer(data=data)
	if serializer.is_valid():
		user = User.objects.create(username=serializer.data.get("username"))
		user.set_password(serializer.data.get("password"))
		user.save()
		return Response(serializer.data, status=200)
	else:
		return Response(serializer.errors, status=400)