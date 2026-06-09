from django.db import models


class Payment(models.Model):
	class Status(models.TextChoices):
		PENDING = 'Pending', 'Pending'
		COMPLETED = 'Completed', 'Completed'
		FAILED = 'Failed', 'Failed'

	order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='payments')
	payment_method = models.CharField(max_length=50)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
	transaction_id = models.CharField(max_length=255, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Payment {self.id}'


class Payout(models.Model):
	vendor = models.ForeignKey('users.Vendor', on_delete=models.CASCADE, related_name='payouts')
	order_item = models.ForeignKey('orders.OrderItem', on_delete=models.CASCADE, related_name='payouts')
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Payout {self.id}'
