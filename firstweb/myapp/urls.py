from django.urls import path, include
from .views import *

urlpatterns = [
    path('', Home,name='home-page'),
    path('about/', About,name='about-page'),
    path('contact/', Contact,name='contact-page'),
    path('vivo-v19/', Vivov19,name='vivo-v19-page'),
    path('addproduct/', AddProduct,name='addproduct-page'),
    path('allproduct/', Product,name='allproduct-page'),
    path('register/', Register,name='register-page'),
    path('addtocart/<int:pid>/',AddtoCart,name='addtocart-page'),
    path('mycart/',MyCart,name='mycart-page'),
    path('mycart/edit/',MyCartEdit,name='mycartedit-page'),
    path('checkout/',Checkout,name='checkout-page'),
    path('orderlist/',OrderlistPage,name='orderlist-page'),
    path('allorderlist/',AllOrderlistPage,name='allorderlist-page')
]
