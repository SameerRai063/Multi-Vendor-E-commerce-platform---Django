from django.db import models


class Category(models.Model):
	name = models.CharField(max_length=255)
	parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

	def __str__(self):
		return self.name


class Product(models.Model):
	vendor = models.ForeignKey('users.Vendor', on_delete=models.PROTECT, related_name='products')
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.PositiveIntegerField(default=0)
	is_available = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name


class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
	image = models.FileField(upload_to='product-images/')

	def __str__(self):
		return f'{self.product.name} image'
