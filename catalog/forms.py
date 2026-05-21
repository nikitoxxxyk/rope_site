from django import forms
from .models import Category, Product, OrderItem, Order

class ProductsFilterForm(forms.Form):
	min_price = forms.IntegerField(
		required=False,
		min_value=0,
		label='Минимальная цена',
		widget=forms.NumberInput(attrs={
			'class': 'form-control',
			'placeholder': 'От'
		})
	)

	max_price = forms.IntegerField(
		required=False,
		min_value=0,
		label='Максимальная цена',
		widget=forms.NumberInput(attrs={
			'class': 'form-control',
			'placeholder': 'До'
		})
	)

	category = forms.ModelChoiceField(
		required=False, 
		queryset=Category.objects.all(),
		empty_label='Все категории',
		label='Категория',
		widget=forms.Select(attrs={
			'class': 'form-control'
		})
	)

	search = forms.CharField(
        required=False,
        label='Поиск',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск товаров...'
        })
    )


class CreateOrderForm(forms.ModelForm):
	customer_name = forms.CharField(
		required=True,
		max_length=100,
		label='Имя',
		widget=forms.TextInput(attrs={
			'class': 'form-control',
			'placeholder': 'Имя'
		})
	)
	
	phone = forms.CharField(
		required=True,
		max_length=100,
		label='Номер телефона',
		widget=forms.TextInput(attrs={
			'class': 'form-control',
			'placeholder': '+79999999999'
		})
	)

	email = forms.EmailField(
		required=False,
		label='Электронная почта',
		widget=forms.EmailInput(attrs={
			'class': 'form-control',
			'placeholder': 'your@email.com'
		})
	)

	comment = forms.CharField(
		required=False,
		label='Комментарий к заказу (необязательно)',
		widget=forms.Textarea(attrs={
			'class': 'form-control',
			'placeholder': 'Введите сообщение',
			'rows': 3
		})
	)

	class Meta:
		model = Order
		fields = ['customer_name', 'phone', 'email', 'comment']


