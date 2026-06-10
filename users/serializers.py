from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'name', 'email', 'phone', 'is_vendor', 'date_joined')
		required_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

	class Meta:
		model = User
		fields = ('id', 'name', 'email', 'phone', 'password')

	def create(self, validated_data):
		password = validated_data.pop('password')
		user = User.objects.create_user(password=password, **validated_data)
		return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)
		token['name'] = user.name
		token['email'] = user.email
		token['is_vendor'] = user.is_vendor
		return token

	def validate(self, attrs):
		data = super().validate(attrs)
		data['user'] = {
			'id': self.user.id,
			'name': self.user.name,
			'email': self.user.email,
			'phone': self.user.phone,
			'is_vendor': self.user.is_vendor,
		}
		return data