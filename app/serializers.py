from rest_framework import serializers
from django.contrib.auth.models import User

class Registration_Serializer(serializers.Serializer):
	username = serializers.CharField(max_length=150)
	password = serializers.CharField(max_length=150)
	email = serializers.EmailField(required=False)

	def validate_username(self, username):
		user = User.objects.filter(username=username).first()
		if user:
			raise serializers.ValidationError("This Username Is Already Taken Before")
		return username

	def validate_email(self, email):
		user = User.objects.filter(email=email).first()
		if user:
			raise serializers.ValidationError("This Email Is Already Taken Before")
		return email
