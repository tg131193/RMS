
from datetime import datetime
from django.shortcuts import render, redirect, HttpResponse
from app.models import Customer, Cart, OrderPlaced,Product

from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm




class ProductView(View):
	def get(self, request):
		totalitem = 0
		
		
		veg= Product.objects.filter(category='V').filter( is_verify=True)
		nonveg= Product.objects.filter(category='NV').filter( is_verify=True)
		frozen= Product.objects.filter(category='F').filter( is_verify=True)
		
		
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		return render(request, 'app/home.html', { 'veg':veg, 'nonveg':nonveg, 'frozen':frozen,})


		
class ProductDetailView(View):
	def get(self, request, pk):
		totalitem = 0
		product = Product.objects.get(pk=pk)
		
		item_already_in_cart=False
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
			item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
		return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

@login_required()
def add_to_cart(request):
	user = request.user
	item_already_in_cart1 = False
	product = request.GET.get('prod_id')
	item_already_in_cart1 = Cart.objects.filter(Q(product=product) & Q(user=request.user)).exists()
	if item_already_in_cart1 == False:
		product_title = Product.objects.get(id=product)
		Cart(user=user, product=product_title).save()
		messages.success(request, 'Product Added to Cart Successfully !!' )
		return redirect('/cart')
	else:
		return redirect('/cart')
 

@login_required
def show_cart(request):
	if request.user.is_authenticated:
		totalitem = 0
		totalitem = len(Cart.objects.filter(user=request.user))
		user = request.user
		cart = Cart.objects.filter(user=user)
		amount =0
		
		shipping_amount =0
		totalamount=0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		print(cart_product)
		if cart_product:
			for p in cart_product:
				#tempamount = (p.quantity * p.product.discounted_price)
				amount+=p.total_cost
				shipping_amount+=p.shipping_ampunt
				totalamount+=p.total
			

				

			return render(request, 'app/addtocart.html', {'carts':cart, 'amount':amount, 'totalamount':totalamount, 'totalitem':totalitem,'shipping_amount':shipping_amount})
		else:
			return render(request, 'app/emptycart.html', {'totalitem':totalitem})
	else:
		return render(request, 'app/emptycart.html', {'totalitem':totalitem})

def plus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity+=1
		c.save()
		amount = 0.0
		

		shipping_amount= 10
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			
			amount += tempamount

			


			if tempamount >= 1 and tempamount <=200:
				shipping_amount=20
			elif tempamount >= 201 and tempamount <=500 :
				shipping_amount=30
			elif tempamount >= 501 and tempamount <=999:
				shipping_amount=40

			elif tempamount >= 1000 and tempamount <=1500:
				shipping_amount=50
			elif tempamount >= 1501 and tempamount <=2000:
				shipping_amount=55
			elif tempamount >= 2001 and tempamount <=2500:
				shipping_amount=60
			elif tempamount >=2501 :
				shipping_amount=65
			
	
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount,
			'shipping_amount':shipping_amount,

		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

def minus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity-=1
		c.save()
		amount = 0.0
		shipping_amount= 0.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			
			amount += tempamount
			tempamount = amount


		if tempamount >= 1 and tempamount <=200:
			shipping_amount=20
		elif tempamount >= 201 and tempamount <=500 :
			shipping_amount=30
		elif tempamount >= 501 and tempamount <=999:
			shipping_amount=40

		elif tempamount >= 1000 and tempamount <=1500:
			shipping_amount=50
		elif tempamount >= 1501 and tempamount <=2000:
			shipping_amount=55
		elif tempamount >= 2001 and tempamount <=2500:
			shipping_amount=60
		elif tempamount >=2501 :
			shipping_amount=65
		
		
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount,
			'shipping_amount':shipping_amount,
			
			
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

#----------------

@login_required

def checkout(request):
	user = request.user
	add = Customer.objects.filter(user=user)
	cart_items = Cart.objects.filter(user=request.user)
	amount = 0.0
	
	shipping_amount=0
	totalamount=0.0
	cart_product = [p for p in Cart.objects.all() if p.user == request.user]
	if cart_product:
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			totalamount+=p.total
			shipping_amount+=p.shipping_ampunt
			amount += tempamount
		tempamount = amount+shipping_amount
		
		
		totalamount = amount+shipping_amount
	return render(request, 'app/checkout.html', {'add':add, 'cart_items':cart_items, 'totalcost':totalamount,'amount':amount,'shipping_amount':shipping_amount,'totalamount':totalamount})

#------------
@login_required
def payment_done(request):
	if request.GET.get('custid'):
	
		custid = request.GET.get('custid')
		print("Customer ID", custid)
		user = request.user
		cartid = Cart.objects.filter(user = user)
		customer = Customer.objects.get(id=custid)
		print(customer)
		for cid in cartid:
			OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
			print("Order Saved")
			cid.delete()
			print("Cart Item Deleted")
		return redirect("orders")
	else:
		return redirect("checkout")

def remove_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.delete()
		amount = 0.0
		shipping_amount= 10
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
		
			amount += tempamount
		
		data = {
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

@login_required
def address(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	add = Customer.objects.filter(user=request.user)
	return render(request, 'app/address.html', {'add':add, 'active':'btn-primary', 'totalitem':totalitem})

@login_required
def orders(request):
	op = OrderPlaced.objects.filter(user=request.user).order_by('-ordered_date')
	

	return render(request, 'app/orders.html', {'order_placed':op})




# detail of product Frozen Food
def frozenfood(request, data=None):
	
	if data==None :
		dryfoods = Product.objects.filter(category='F')
	elif data == '' or data == '':
		dryfoods = Product.objects.filter(category='F').filter(brand=data)
	elif data == 'below':
		dryfoods = Product.objects.filter(category='F').filter(discounted_price__lt=300)
	elif data == 'above':
		dryfoods = Product.objects.filter(category='F').filter(discounted_price__gt=300)
	return render(request, 'app/froze.html', {'dryfoods':dryfoods})
#end
# detail of product nonveg
def nonveg(request, data=None):
	
	if data==None :
		foods = Product.objects.filter(category='NV')
	elif data == '' or data == '':
		foods = Product.objects.filter(category='NV').filter(brand=data)
	elif data == 'below':
		foods = Product.objects.filter(category='NV').filter(discounted_price__lt=500)
	elif data == 'above':
		foods = Product.objects.filter(category='NV').filter(discounted_price__gt=500)
	return render(request, 'app/food.html', {'foods':foods,})
#end
# detail of product veg
def veg(request, data=None):
	
	if data==None :
			drink = Product.objects.filter(category='V')
	elif data == '' or data == '':
			drink = Product.objects.filter(category='V').filter(brand=data)
	elif data == 'below':
			drink = Product.objects.filter(category='V').filter(discounted_price__lt=500)
	elif data == 'above':
			drink= Product.objects.filter(category='V').filter(discounted_price__gt=500)
	return render(request, 'app/veg.html', {'veg':drink,})
#end





class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form':form})
  
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  
  
  if form.is_valid():
   form.save()
   messages.success(request, 'Congratulations!! Registered Successfully.')
  return render(request, 'app/customerregistration.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
	def get(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm()
		return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
		
	def post(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			usr = request.user
			name  = form.cleaned_data['name']
			phone = form.cleaned_data['phone']
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			reg = Customer(user=usr, name=name,phone=phone, locality=locality, city=city, state=state, zipcode=zipcode)
			reg.save()
			messages.success(request, 'Congratulations!! Profile Updated Successfully.')
		return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})




# Login View Function
def user_login(request):
  if not request.user.is_authenticated:
    if request.method == "POST":
		
      fm = AuthenticationForm(request=request, data=request.POST)
      if fm.is_valid():
        uname = fm.cleaned_data['username']
        upass = fm.cleaned_data['password']
        user = authenticate(username=uname, password=upass)
        if user is not None:
          login(request, user)
          messages.success(request, 'Logged in successfully !!')
          return redirect('/profile/')
    else: 
      fm = AuthenticationForm()
    return render(request, 'enroll/userlogin.html', {'form':fm})
  else:
    return redirect('/profile/')