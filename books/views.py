from django.shortcuts import render,get_object_or_404,redirect
from .models import Book, Category, Other, Order, OrderItem
from django.core.paginator import Paginator
from .forms import ReviewForm, RegistrationForm,OrderForm,OrderItemForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView,LogoutView

# Create your views here.
def book_list(request):
    category_id = request.GET.get('category_id')
    categories = Category.objects.all()
    search_query = request.GET.get('search')

    if category_id:
        books = Book.objects.filter(category_id=category_id)
    else:
        books = Book.objects.all()
    if search_query:
        books = books.filter(title__icontains=search_query)

    pagination = Paginator(books, 15)
    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)
    return render(request, 'books/book_list.html', {'books': page_obj,'categories': categories,  'page_obj': page_obj})

def category_book(request):
    newBooks = Book.objects.extra(where=["\"books_book\".\"isNew\" = 'True'"])[:6]
    setBooks = Book.objects.extra(where=["\"books_book\".\"isSet\" = 'True'"])[:6]
    recommendedBooks = Book.objects.extra(where=["\"books_book\".\"isRecommended\" = 'True'"])[:6]
    categories = Category.objects.all()
    return render(request, 'books/book_list_category.html', {'newBooks': newBooks, 'setBooks': setBooks,'recommendedBooks': recommendedBooks, 'categories': categories})

def book_detail(request,id):
    book = get_object_or_404(Book, id=id)
    categories = Category.objects.all()
    reviews = book.reviews.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.save()
            return redirect('book_detail', id=book.id)
    else:
        form = ReviewForm()

    return render(request, 'books/book_detail.html', {'book': book, 'categories' : categories,'reviews': reviews,'form': form})

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for key, quantity in cart.items():
        model_type, item_id = key.split('_')
        if model_type == 'Book':
            item = Book.objects.get(id=item_id)
        elif model_type == 'Other':
            item = Other.objects.get(id=item_id)
        else:
            continue

        cart_items.append({
            'item': item,
            'quantity': quantity,
            'model_type': model_type,
            'subtotal': item.price * quantity,
        })
        total_price += item.price * quantity
    return render(request, 'books/cart.html', {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request, model_type, item_id):
    cart = request.session.get('cart', {})
    key = f"{model_type}_{item_id}" 
    cart[key] = cart.get(key,0) + 1
    request.session['cart'] = cart
    return redirect('cart_view')

def remove_from_cart(request, model_type, item_id):
    cart = request.session.get('cart', {})
    key = f"{model_type}_{item_id}" 
    if key in cart:
        del cart[key]
        request.session['cart'] = cart
    return redirect('cart_view')

def gift_list(request):
    gifts = Other.objects.extra(where=["\"books_other\".\"is_gift\" = 'True'"])
    return render(request, 'books/gift_list.html', {'gifts': gifts})

def game_list(request):
    games = Other.objects.extra(where=["\"books_other\".\"is_game\" = 'True'"])
    return render(request, 'books/game_list.html', {'games': games})

def notebook_list(request):
    notebooks = Other.objects.extra(where=["\"books_other\".\"is_notebook\" = 'True'"])
    return render(request, 'books/notebook_list.html', {'notebooks': notebooks})

def other_detail(request,id):
    other = get_object_or_404(Other, id=id)
    return render(request, 'books/other_detail.html', {'other': other})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('category_book')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        request.session.flush() 
        return super().dispatch(request, *args, **kwargs)
    

def create_order(request):
    cart = request.session.get('cart', {})  # Отримати кошик із сесії
    if not cart:
        return render(request, 'empty_cart.html')  # Показати повідомлення, якщо кошик порожній

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            # Створити замовлення
            order = order_form.save(commit=False)
            order.user = request.user
            order.save()

            # Додати товари з кошика до замовлення
            for key, quantity in cart.items():
                try:
                    # Витягнути тип моделі та ID товару з ключа
                    model_type, item_id = key.split("_")
                    item_id = int(item_id)

                    if model_type == "Book":
                        product = Book.objects.get(id=item_id)
                    elif model_type == "Other":
                        product = Other.objects.get(id=item_id)
                    else:
                        continue  # Пропустити, якщо модель невідома

                    # Створити OrderItem
                    OrderItem.objects.create(
                        order=order,
                        book=product if model_type == 'book' else None,
                        other=product if model_type == 'other' else None,
                        quantity=quantity,
                        unit_price=product.price,
                    )
                except (Book.DoesNotExist, Other.DoesNotExist):
                    continue

            # Очистити кошик після створення замовлення
            request.session['cart'] = {}
            return redirect('order_success')  # Перенаправлення після успіху

    else:
        order_form = OrderForm()

    # Підготувати товари для відображення у шаблоні
    items = []
    total_cost = 0
    for key, quantity in cart.items():
        model_type, item_id = key.split("_")
        item_id = int(item_id)

        if model_type == "Book":
            try:
                product = Book.objects.get(id=item_id)
                items.append({
                    'title': product.title,
                    'price': product.price,
                    'quantity': quantity,
                    'total': product.price * quantity,
                })
                total_cost += product.price * quantity
            except Book.DoesNotExist:
                continue

        elif model_type == "Other":
            try:
                product = Other.objects.get(id=item_id)
                items.append({
                    'title': product.title,
                    'price': product.price,
                    'quantity': quantity,
                    'total': product.price * quantity,
                })
                total_cost += product.price * quantity
            except Other.DoesNotExist:
                continue

    return render(request, 'create_order.html', {
        'order_form': order_form,
        'items': items,
        'total_cost': total_cost,
    })


def order_success(request):
    return render(request, 'order_success.html')