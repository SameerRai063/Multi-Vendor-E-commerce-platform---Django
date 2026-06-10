from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class JwtAuthTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			email='buyer@example.com',
			name='Buyer User',
			password='StrongPass123!',
			phone='1234567890',
		)
		self.vendor = User.objects.create_user(
			email='vendor@example.com',
			name='Vendor User',
			password='StrongPass123!',
			phone='0987654321',
			is_vendor=True,
		)

	def test_token_obtain_pair_returns_tokens_and_user_payload(self):
		response = self.client.post(
			reverse('token_obtain_pair'),
			{'email': 'buyer@example.com', 'password': 'StrongPass123!'},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('access', response.data)
		self.assertIn('refresh', response.data)
		self.assertEqual(response.data['user']['email'], 'buyer@example.com')

	def test_me_requires_jwt_and_returns_current_user(self):
		response = self.client.post(
			reverse('token_obtain_pair'),
			{'email': 'buyer@example.com', 'password': 'StrongPass123!'},
			format='json',
		)

		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
		me_response = self.client.get(reverse('me'))

		self.assertEqual(me_response.status_code, status.HTTP_200_OK)
		self.assertEqual(me_response.data['email'], 'buyer@example.com')

	def test_vendor_endpoint_allows_vendors_only(self):
		response = self.client.post(
			reverse('token_obtain_pair'),
			{'email': 'vendor@example.com', 'password': 'StrongPass123!'},
			format='json',
		)

		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
		vendor_response = self.client.get(reverse('vendor_me'))

		self.assertEqual(vendor_response.status_code, status.HTTP_200_OK)
		self.assertEqual(vendor_response.data['email'], 'vendor@example.com')

	def test_customer_endpoint_rejects_vendor_users(self):
		response = self.client.post(
			reverse('token_obtain_pair'),
			{'email': 'vendor@example.com', 'password': 'StrongPass123!'},
			format='json',
		)

		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
		customer_response = self.client.get(reverse('customer_me'))

		self.assertEqual(customer_response.status_code, status.HTTP_403_FORBIDDEN)

	def test_register_creates_a_user(self):
		response = self.client.post(
			reverse('register'),
			{
				'name': 'New User',
				'email': 'new@example.com',
				'phone': '5551234567',
				'password': 'StrongPass123!',
			},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(User.objects.filter(email='new@example.com').exists())
