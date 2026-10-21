from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Product, Category, Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)

@admin.register(Product)
class ProductAdmin(ModelAdmin):
	list_display = ['name', 'category', 'quantity', 'length', 'price', 'diameter', 'weight', 'quantity_in_pack']
	search_fields = ['name']
	prepopulated_fields = {
		'slug': ('name',)
	}

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
	prepopulated_fields = {'slug': ('name',),}
	list_display = ('name', 'slug')
	search_fields = ('name',)

