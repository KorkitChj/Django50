from django.shortcuts import render
from django.http import HttpResponse
from .models import Allproduct

def Home(request):
	product1 = 'Smartphone'
	product2 = 'Notebook'
	product3 = 'Software'

	context = {'product1':product1,'product2':product2,'product3':product3}

	return render(request, 'myapp/home.html',context)

	#eturn HttpResponse('<h1 style="color:red">สวัสดี Hello World</h1><p>สบายดีไหม</p>') 

def About(request):
	return render(request, 'myapp/about.html')

def Contact(request):
	return render(request, 'myapp/contact.html')

def Vivov19(request):
	return render(request, 'myapp/vivo-v19.html')

from .models import Allproduct

def AddProduct(request):
	if request.method == 'POST':
		data = request.POST.copy()
		name = data.get('name')
		price  = data.get('price')
		detail = data.get('detail')
		imageurl = data.get('imageurl')

		new = Allproduct()
		new.name = name
		new.price = price
		new.detail = detail
		new.imageurl = imageurl
		new.save()

	return render(request, 'myapp/addproduct.html')

def Product(request):
	product = Allproduct.objects.all()
	context = {'product':product}
	return render(request, 'myapp/allproduct.html',context)