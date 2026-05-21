from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, Category, Order, OrderItem
import json
from .forms import CreateOrderForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages

def home_view(request):
	products = Product.objects.order_by('created_at')[:6]
	context = {
		'products': products
	}

	return render(request, 'index.html', context)

def catalog_view(request):
	products = Product.objects.all()
	categories = Category.objects.all()

	# Фильтрация по категории
	category_slug = None
	if request.method == 'GET':
		category_slug = request.GET.get('slug')

	selected_category = None
	if category_slug:
		try:
			selected_category = categories.get(slug=category_slug)
			products = products.filter(category=selected_category)
		except Category.DoesNotExist:
			selected_category = None

	# Фильтрация по цене
	min_price = request.GET.get('min_price')
	max_price = request.GET.get('max_price')

	if min_price:
		products = products.filter(price__gte=float(min_price))
	if max_price:
		products = products.filter(price__lte=float(max_price))

	# Фильтрация по диаметру
	min_diam = request.GET.get('min_diameter')
	max_diam = request.GET.get('max_diameter')

	if min_diam:
		try:
			products = products.filter(diameter__gte=float(min_diam))
		except ValueError:
			pass
	if max_diam:
		products = products.filter(diameter__lte=max_diam)

	context = {
		'products': products,
		'categories': categories,
		'selected_category': selected_category
	}

	return render(request, 'catalog.html', context)

def add_to_cart(request, product_id):
	product = get_object_or_404(Product, id=product_id) # получаем товар по id либо ошибку 404, если его нет

	cart = request.session.get('cart', {}) # получаем корзину из сессии, если ее еще нет то создаем новую

	product_key = str(product_id)
	if product_key in cart:
		cart[product_key]['quantity'] += 1
	else:
		cart[product_key] = {
			'name': product.name,
			'price': str(product.price),
			'quantity': 1,  # ПОКА НЕПОНЯТНО КАК БУДЕМ РЕАЛИЗОВЫВАТЬ КОЛИЧЕСТВО ТОВАРОВ
			'image': product.image.url if product.image else '',
		}

	request.session['cart'] = cart
	return redirect('catalog')

def cart_view(request):
	cart = request.session.get('cart', {}) # Получаем из сессии корзину
	
	cart_items = [] # Список с хранением товаров и их количеством

	for product_id, item_data in cart.items():
		try:
			product = Product.objects.get(id=int(product_id))

			cart_items.append({
				'product': product,
				'quantity': item_data['quantity'],
				'total_price': product.price * item_data['quantity']
			})
		except Product.DoesNotExist: # Если товар удален из базы данных - пропускаем
			continue

	total_sum = sum(item['total_price'] for item in cart_items)

	form = CreateOrderForm()

	context = {
		'cart_items': cart_items,
		'total_sum': total_sum,
		'form': form
	}
	
	return render(request, 'cart.html', context)

def delete_from_cart(request, product_id):
	if request.method == "POST":
		cart = request.session.get('cart', {})
		new_cart = {}
		for product_key, item_data in cart.items():
			if product_key != str(product_id):
				new_cart[product_key] = item_data
		
		request.session['cart'] = new_cart
	
	return redirect('cart')

def order_success(request):
	return render(request, 'order_success.html')

def send_order_email(order):
	items = order.items.all()

	context = {
		'order': order,
		'items': items,
		'total': sum(item.quantity * item.price for item in items)
	}

	html_message = render_to_string('email/order_email.html', context)
	plain_message = render_to_string('email/order_email.txt', context)

	# Отправка на почту kapron.by@gmail.com
	send_mail(
        subject=f'Новый заказ #{order.id}',
        message=plain_message,
        from_email='lentamarket92@gmail.com',
        recipient_list=['lentamarket92@gmail.com'],
		# recipient_list=['rodstvennik@yandex.ru', order.email] - дублировать клиенту
		html_message=html_message,
		fail_silently=False,
	)

def create_order(request):
	if request.method == 'POST':
		form = CreateOrderForm(request.POST)
		cart = request.session.get('cart', {})
		if cart and form.is_valid():
			order = form.save()
			for product_id, item_data in cart.items():
				product = get_object_or_404(Product, id=int(product_id))

				OrderItem.objects.create(
					order=order,
					product=product,
					quantity=item_data['quantity'],
					price=item_data['price'],
				)

			request.session['cart'] = {}
		
			send_order_email(order)

			return redirect('order_success')
		else:
			return redirect('cart')
			
	else:
		return redirect('cart')

def payment_delivery(request):
	return render(request, 'payment_delivery.html')

def contact_view(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		message = request.POST.get('message')

		subject = f"Вопрос с сайта от {name}"
		body = f"""
				Имя: {name} 
				Email: {email} 
				Телефон: {phone} 
				Вопрос: {message}
				"""

		try:
			send_mail(
				subject=subject,
				message=body,
				from_email='lentamarket92@gmail.com',
				recipient_list=['lentamarket92@gmail.com'],
				fail_silently=False,
				)
			return render(request, 'contact_success.html')
		
		except Exception as e:
			messages.error(request, 'Ошибка при отправке. Попробуйте позже.')
	
	return redirect('home')

def call_request(request):
	if request.method == "POST":
		name = request.POST.get('name')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		message = request.POST.get('message')

		subject = f"Заказ звонка от {name}"
		body = f"""
			Заказ звонка от {name}
			
			Имя: {name}
			Email: {email if email else 'Не указан'}
			Телефон: {phone}

			Сообщение: 
			{message if message else '-'}
		"""

		try:
			send_mail(
				subject=subject,
				message=body,
				from_email='lentamarket92@gmail.com',
				recipient_list=['lentamarket92@gmail.com'],
				fail_silently=False,
			)
			return render(request, 'call_success.html')
			# messages.success(request, 'Спасибо! Мы свяжемся с вами в ближайшее время.')
		except Exception as e:
			return render(request, 'call_error.html')
			# messages.error(request, 'Ошибка при отправке. Попробуйте позже.')
		
	return render(request, 'call_request.html')		
	
