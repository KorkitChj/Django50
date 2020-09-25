from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.files.storage import FileSystemStorage  # ไว้เก็บรูป
from django.contrib.auth.models import User  # เกี่ยวกับ user
from django.contrib.auth import authenticate, login
from datetime import datetime

def Home(request):
	product = Allproduct.objects.all().order_by(
		'id').reverse()[:3]  # [:3] น้อยกว่า 3
	preorder = Allproduct.objects.filter(quantity__lte=0)
	# quantity__lte=0 (หาค่าที่มี quantity <= 0 - lte is <=) (underscore 2 ตัว)
	# quantity__gt=0  (หาค่าที่มี quantity > 0 - gt is >)
	# quantity__gte=0  (หาค่าที่มี quantity >= 5 -  gte is >=)
	context = {'product': product, 'preorder': preorder}

	return render(request, 'myapp/home.html', context)

	# eturn HttpResponse('<h1 style="color:red">สวัสดี Hello World</h1><p>สบายดีไหม</p>')


def About(request):
	return render(request, 'myapp/about.html')


def Contact(request):
	return render(request, 'myapp/contact.html')


def Vivov19(request):
	return render(request, 'myapp/vivo-v19.html')

# from .models import Allproduct


def AddProduct(request):
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')

		if request.method == 'POST' and request.FILES['imageupload']:
			data = request.POST.copy()
			name = data.get('name')
			price = data.get('price')
			detail = data.get('detail')
			imageurl = data.get('imageurl')
			quantity = data.get('quantity')
			unit = data.get('unit')

			new = Allproduct()
			new.name = name
			new.price = price
			new.detail = detail
			new.imageurl = imageurl
			new.quantity = quantity
			new.unit = unit
			# Save Image
			file_image = request.FILES['imageupload']
			file_image_name = request.FILES['imageupload'].name.replace(
				' ', '')
			print('FILE_IMAGE:', file_image)
			print('IMAGE_NAME:', file_image_name)
			fs = FileSystemStorage()
			filename = fs.save(file_image_name, file_image)
			upload_file_url = fs.url(filename)  # "media/xxxx.png"
			# "[6:]" เป็นการเอาตัวอักษรตัวที่ 6 ขึ้นไป "xxxx.png"
			new.image = upload_file_url[6:]
			##############################
			new.save()

	return render(request, 'myapp/addproduct.html')


def Product(request):

	product = Allproduct.objects.all().order_by('id').reverse()
	context = {'product': product}
	return render(request, 'myapp/allproduct.html', context)


def Register(request):
	if request.method == 'POST':
		data = request.POST.copy()
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		email = data.get('email')
		password = data.get('password')
		# ยังไม่ใส่ try except เพื่อป้องกันการสมัครซ้ำ
		# +alert ไปหน้าสมัครว่าอีเมลล์นี้เคยสมัครแล้ว
		# สอน คู่กับหัวข้อ reset password
		newuser = User()
		newuser.username = email
		newuser.email = email
		newuser.first_name = first_name
		newuser.last_name = last_name
		newuser.set_password(password)
		newuser.save()

		profile = Profile()
		profile.user = User.objects.get(username=email)
		profile.save()

		user = authenticate(username=email, password=password)
		login(request, user)

	return render(request, 'myapp/register.html')


def AddtoCart(request, pid):
	# localhost:8000/addtocart/3
	# {% url 'addtocart-page' pd.id %}
	print(request.user)
	username = request.user.username
	user = User.objects.get(username=username)
	check = Allproduct.objects.get(id=pid)

	try:
		newcart = Cart.objects.get(user=user, productid=str(pid))
		#print('EXITS: ',pcheck.exists())
		newquan = newcart.quantity + 1
		newcart.quantity = newquan
		calculate = newcart.price * newquan
		newcart.total = calculate
		newcart.save()

		# update จำนวนตระกร้าสินค้า ณ ตอนนี้
		count = Cart.objects.filter(user=user)
		count = sum([c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

		return redirect('allproduct-page')
	except:
		newcart = Cart()
		newcart.user = user
		newcart.productid = pid
		newcart.productname = check.name
		newcart.price = int(check.price)
		newcart.quantity = 1
		calculate = int(check.price) * 1
		newcart.total = calculate
		newcart.save()

		# update จำนวนตระกร้าสินค้า ณ ตอนนี้
		count = Cart.objects.filter(user=user)
		count = sum([c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

		return redirect('allproduct-page')


def MyCart(request):
	username = request.user.username
	user = User.objects.get(username=username)

	context = {}

	# ใช้สำหรับการลบ
	if request.method == 'POST':
		data = request.POST.copy()
		productid = data.get('productid')
		item = Cart.objects.get(user=user, productid=productid)
		item.delete()
		context['status'] = 'delete'

		count = Cart.objects.filter(user=user)
		count = sum([c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

	username = request.user.username
	user = User.objects.get(username=username)
	mycart = Cart.objects.filter(user=user)
	count = sum([c.quantity for c in mycart])
	total = sum([c.total for c in mycart])
	context['mycart'] = mycart
	context['count'] = count
	context['total'] = total
	return render(request, 'myapp/mycart.html', context)


def MyCartEdit(request):
	username = request.user.username
	user = User.objects.get(username=username)

	context = {}

	if request.method == 'POST':
		data = request.POST.copy()
		# print(data)
		if data.get('clear') == 'clear':
			print(data.get('clear'))
			Cart.objects.filter(user=user).delete()
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquan = 0
			updatequan.save()
			return redirect('mycart-page')

		editlist = []
		for k, v in data.items():
			print([k, v])
			if k[:2] == 'pd':
				pid = int(k.split('_')[1])
				dt = [pid, int(v)]
				editlist.append(dt)
		print('EDITLIST', editlist)  # [[9,10],[7,8]] 9=productid 10=quan

		for ed in editlist:
			edit = Cart.objects.get(productid=ed[0], user=user)  # productis
			edit.quantity = ed[1]  # quan
			calculate = edit.price * ed[1]
			edit.total = calculate
			edit.save()

		count = Cart.objects.filter(user=user)
		count = sum([c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
		return redirect('mycart-page')
		# if data.get('checksave') == 'checksave':
		#	return redirect('mycart-page')

	mycart = Cart.objects.filter(user=user)
	context['mycart'] = mycart
	return render(request, 'myapp/mycartedit.html', context)


def Checkout(request):
		if request.method == 'POST':
			username = request.user.username
			user = User.objects.get(username=username)
			data = request.POST.copy()
			name = data.get('name')
			tel = data.get('tel')
			address = data.get('address')
			shipping = data.get('shipping')
			payment = data.get('payment')
			other = data.get('other')
			page = data.get('page')
			if page == 'information':
				context = {}
				context['name'] = name
				context['tel'] = tel
				context['address'] = address
				context['shipping'] = shipping
				context['payment'] = payment
				context['other'] = other

				mycart = Cart.objects.filter(user=user)
				count = sum([c.quantity for c in mycart])
				total = sum([c.total for c in mycart])
				context['mycart'] = mycart
				context['count'] = count
				context['total'] = total

				return render(request, 'myapp/checkout2.html',context)
			if page == 'confirm':
				print('Confirm')
				print(data)
				mycart = Cart.objects.filter(user=user)

				mid = str(user.id).zfill(4)
				dt = datetime.now().strftime('%Y%m%d%H%M%S')
				orderid = 'OD' + mid + dt

				for pd in mycart:
					order = Orderlist()
					order.orderid =  orderid
					order.productid = pd.productid
					order.productname = pd.productname
					order.price = pd.price
					order.quantity = pd.quantity
					order.total = pd.total
					order.save()


				#create order pending
				odp =  OrderPending()
				odp.orderid = orderid
				odp.user = user
				odp.name = name
				odp.tel = tel
				odp.address = address
				odp.shipping = shipping
				odp.payment = payment
				odp.other = other
				odp.save()

				#clear cart
				Cart.objects.filter(user=user).delete()
				updatequan = Profile.objects.get(user=user)
				updatequan.cartquan = 0
				updatequan.save()
				return redirect('mycart-page')

				# generate orther no. and save to Order Models
				# save product in cart to OrderProduct models
				# clear cart
				# redirect to order list page

		return render(request, 'myapp/checkout1.html')


def OrderlistPage(request):
	username = request.user.username
	user = User.objects.get(username=username)

	context = {}
	order = OrderPending.objects.filter(user=user)

	for od in order:
		orderid = od.orderid
		odlist = Orderlist.objects.filter(orderid=orderid)
		total = sum([c.total for c in odlist])
		od.total = total

	context['allorder'] = order

	return render(request, 'myapp/orderlist.html',context)

def AllOrderlistPage(request):

	context = {}
	order = OrderPending.objects.all()

	for od in order:
		orderid = od.orderid
		odlist = Orderlist.objects.filter(orderid=orderid)
		total = sum([c.total for c in odlist])
		od.total = total

	context['allorder'] = order

	return render(request, 'myapp/allorderlist.html',context)
