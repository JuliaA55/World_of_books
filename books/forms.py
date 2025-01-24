from django import forms
from .models import Review,Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author', 'content', 'rating']
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': "Ваше ім'я"
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Ваш відгук'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 1, 
                'max': 5, 
                'placeholder': 'Враження від 1 до 5'
            })  
        }
        labels = {
            'author': 'Автор',
            'content': 'Зміст',
            'rating': 'Враження(1-5)',
        }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Ім\'я користувача',
            'email': 'Електронна пошта',
            'password1': 'Пароль',
            'password2': 'Підтвердження пароля',
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'phone_number']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'shipping_address': 'Адреса доставки',
            'phone_number': 'Номер телефона',
        }


class OrderItemForm(forms.Form):
    product_type = forms.ChoiceField(
        choices=[('book', 'Книга'), ('other', 'Інше')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))