from django.urls import path
from . import views

urlpatterns = [
    path('',views.store, name='store'),
    path('cart/',views.cart, name='cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('update_cart/',views.updateCart, name='update_cart'),
    path('process_order/',views.processOrder, name='process_order'),
]
