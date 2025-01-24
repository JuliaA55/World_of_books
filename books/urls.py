from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.category_book, name='category_book'),
    path('<int:id>/', views.book_detail, name='book_detail'),
    path('books/', views.book_list, name='book_list'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<str:model_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<str:model_type>/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('gifts/', views.gift_list, name='gift_list'),
    path('games/', views.game_list, name='game_list'),
    path('notebooks/', views.notebook_list, name='notebook_list'),
    path('other/<int:id>/', views.other_detail, name='other_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/',  views.CustomLogoutView.as_view(next_page='/login/'), name='logout'),
    path('orders/', views.create_order, name='create_order'),
    path('order/', views.order_success, name='order_success'),
]