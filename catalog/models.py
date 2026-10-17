from django.db import models
from django.template.defaultfilters import slugify

class Product(models.Model):
	# Обязательны
	name = models.CharField(max_length=250, verbose_name='Наименование')
	category = models.ForeignKey('Category', verbose_name='Категория', related_name='products', on_delete=models.CASCADE)
	slug = models.SlugField(max_length=300, verbose_name='URL', blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

	# Не у всех товаров есть
	quantity = models.CharField(verbose_name='Количество (м)', max_length=300, blank=True, null=True)
	description = models.TextField(verbose_name='Описание', blank=True)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
	in_stock = models.BooleanField(verbose_name='В наличии', default=True)
	meters_in_pack = models.PositiveIntegerField(null=True, blank=True, verbose_name="Длина (м)", )
	color = models.CharField(verbose_name="Цвет", blank=True, max_length=100)
	packaging = models.CharField(max_length=100, blank=True, verbose_name="Упаковка")
	quantity_in_pack = models.CharField(max_length=100, blank=True, verbose_name="Упаковка")
	breaking_load = models.FloatField(null=True, blank=True, verbose_name='Разрывная нагрузка (кгс)')
	length = models.CharField(max_length=100, blank=True, verbose_name="Длина")
	weight = models.CharField(max_length=100, blank=True, verbose_name="Вес")
	price_unit = models.CharField(
		max_length=20,
		choices=[
			('м', 'руб./метр'),
            ('кг', 'руб./кг'),
            ('шт', 'руб./шт.'),
		],
		default='м',
		verbose_name='Единица цены'
	)

	is_new = models.BooleanField(default=True, verbose_name='Новая позиция')
	is_featured = models.BooleanField(default=True, verbose_name="Популярное")
	diameter = models.FloatField(null=True, blank=True, verbose_name='Диаметр (мм)', help_text='При написании чисел с плавающей запятой используйте точку (.)')
	packaging_type = models.CharField(max_length=100, blank=True, null=True, verbose_name='Вид упаковки')
	length_in_pack = models.CharField(max_length=100, blank=True, null=True, verbose_name='Кол-во в упаковке (м)')

	class Meta:
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'
		ordering = ['-created_at']

	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super().save(*args, **kwargs)

class Category(models.Model):
	name = models.CharField(max_length=250, verbose_name='Категория', unique=True)
	slug = models.SlugField(max_length=300, unique=True, verbose_name='URL', blank=True)
	image = models.ImageField(upload_to='products/', verbose_name='Изображение', blank=True, null=True)

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

class Order(models.Model):
	customer_name = models.CharField(max_length=250, verbose_name='Имя')
	phone = models.CharField(max_length=50, verbose_name='Телефон')
	email = models.EmailField(verbose_name='E-mail', blank=True)
	comment = models.TextField(verbose_name='Комментарий', blank=True)

	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
	is_processed = models.BooleanField(default=False, verbose_name='Обработан')

	products = models.ManyToManyField(Product, through='OrderItem')

	class Meta:
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'
		ordering = ['-created_at']

	def __str__(self):
		return f'Заказ от {self.customer_name} - {self.created_at.strftime("%d.%m.%Y")}'
	
class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена на момент заказа')

	def __str__(self):
		return f'{self.product.name} x {self.quantity}'
	
	class Meta:
		verbose_name = 'Заказанные товары'
		verbose_name_plural = 'Заказанные товары'


	
	