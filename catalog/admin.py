from django.contrib import admin
from .models import Product, Category, Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'category', 'quantity', 'price', 'diameter', 'breaking_load_display', 'breaking_load_kg', 'packaging_type', 'length_in_pack']
	search_fields = ['name']
	prepopulated_fields = {
		'slug': ('name',)
	}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',),}
	list_display = ('name', 'slug')
	search_fields = ('name',)

