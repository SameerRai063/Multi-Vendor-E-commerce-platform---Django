from django.db import models


class Cart(models.Model):
	user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='carts')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Cart {self.id}'


class CartItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='cart_items')
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return f'{self.product.name} x {self.quantity}'


class Order(models.Model):
	class Status(models.TextChoices):
		PENDING = 'Pending', 'Pending'
		SHIPPED = 'Shipped', 'Shipped'
		DELIVERED = 'Delivered', 'Delivered'
		CANCELLED = 'Cancelled', 'Cancelled'

	user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='orders')
	total_amount = models.DecimalField(max_digits=10, decimal_places=2)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
	shipping_address = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Order {self.id}'


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='order_items')
	vendor = models.ForeignKey('users.Vendor', on_delete=models.PROTECT, related_name='order_items')
	quantity = models.PositiveIntegerField(default=1)
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f'{self.product.name} x {self.quantity}'
