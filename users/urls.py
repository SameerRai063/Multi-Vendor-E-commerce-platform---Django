from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CustomerMeView, CustomTokenObtainPairView, MeView, RegisterView, VendorMeView

urlpatterns = [
	path('register/', RegisterView.as_view(), name='register'),
	path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('me/', MeView.as_view(), name='me'),
	path('vendor/me/', VendorMeView.as_view(), name='vendor_me'),
	path('customer/me/', CustomerMeView.as_view(), name='customer_me'),
]