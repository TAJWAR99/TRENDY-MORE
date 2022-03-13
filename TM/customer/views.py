from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json,datetime
from .models import Product, Order, OrderItem, ShippingAddress
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def store(request):
	product = Product.objects.all()
	if request.user.is_authenticated:
		customer = request.user.customer # User and Customer one to one relation
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'get_cart_item':0,'get_cart_total':0}

	context = {'products':product, 'order':order}
	return render(request,'store/store.html', context)
	#return HttpResponse('<h1>Home</h1>')

def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer # User and Customer one to one relation
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()

	else:
		items = []
		order = {'get_cart_item':0,'get_cart_total':0}

	context = {'items':items, 'order':order}
	return render(request,'store/cart.html',context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'get_cart_item':0,'get_cart_total':0}


	context = {'items':items, 'order':order}
	return render(request,'store/checkout.html',context)

def updateCart(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print(productId,action)
	customer = request.user.customer

	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer)
	orderItems, created = OrderItem.objects.get_or_create(order=order,product=product)

	if action == 'add':
		orderItems.quantity = orderItems.quantity + 1
	elif action == 'remove':
		orderItems.quantity = orderItems.quantity - 1

	orderItems.save()
	if orderItems.quantity <= 0:
		orderItems.delete()

	return JsonResponse("hello",safe=False)

@csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		order.transaction_id = transaction_id
		total = float(data['form']['total'])

		if total == order.get_cart_total:
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
				customer=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
			)
	else:
		print('User is not logged in')

	return JsonResponse("Transaction complete",safe=False)


