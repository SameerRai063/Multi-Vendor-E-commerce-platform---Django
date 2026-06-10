from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsCustomer, IsVendor
from .serializers import CustomTokenObtainPairSerializer, RegisterSerializer, UserSerializer


User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
	serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
	queryset = User.objects.all()
	permission_classes = [permissions.AllowAny]
	serializer_class = RegisterSerializer


class MeView(generics.RetrieveAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = UserSerializer

	def get_object(self):
		return self.request.user


class VendorMeView(generics.RetrieveAPIView):
	permission_classes = [permissions.IsAuthenticated, IsVendor]
	serializer_class = UserSerializer

	def get_object(self):
		return self.request.user


class CustomerMeView(generics.RetrieveAPIView):
	permission_classes = [permissions.IsAuthenticated, IsCustomer]
	serializer_class = UserSerializer

	def get_object(self):
		return self.request.user
