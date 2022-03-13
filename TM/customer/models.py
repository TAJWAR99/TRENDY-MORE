from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=50, null=True, blank=True)
	email = models.EmailField(max_length=100, null=True, blank=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=200, null=True, blank=True)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	digital = models.BooleanField(default=False, null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	
	def __str__(self):
		return self.name

	#it will work as a attribute of Product class
	@property
	def imageUrl(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url


class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	complete = models.BooleanField(default=False, null=True, blank=True)
	transaction_id = models.CharField(max_length=200, null=True)
	date_ordered = models.DateTimeField(auto_now_add=True)

	@property
	def shipping(self):
		shipping = False
		orderItems = self.orderitem_set.all()
		for i in orderItems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_item(self):
		orderItems = self.orderitem_set.all() #as OrderItem is child of Order
		total = sum([q.quantity for q in orderItems]) #Adding the quantity of orderItems
		return total

	@property
	def get_cart_total(self):
		orderItems = self.orderitem_set.all() #as OrderItem is child of Order
		total = sum([i.get_total for i in orderItems]) 
		return total


class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.quantity*self.product.price
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	address = models.CharField(max_length=200, null=True, blank=True)
	city = models.CharField(max_length=200, null=True, blank=True)
	state = models.CharField(max_length=200, null=True, blank=True)
	zipcode = models.CharField(max_length=200, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
