from rest_framework import permissions


class IsVendor(permissions.BasePermission):
	message = 'Vendor access is required.'

	def has_permission(self, request, view):
		return bool(request.user and request.user.is_authenticated and request.user.is_vendor)


class IsCustomer(permissions.BasePermission):
	message = 'Customer access is required.'

	def has_permission(self, request, view):
		return bool(request.user and request.user.is_authenticated and not request.user.is_vendor)