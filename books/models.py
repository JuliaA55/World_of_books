from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    genre = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    isNew = models.BooleanField()
    isSet = models.BooleanField(default=False)
    isRecommended = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    price = models.IntegerField(null=True, blank=True)
    edition = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, related_name='books')

    def __str__(self):
        return self.title

class Other(models.Model):
    title = models.CharField(max_length=200)
    edition = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=100)
    is_game = models.BooleanField(default=False)
    is_gift = models.BooleanField(default=False)
    is_notebook = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.author} ({self.rating}/5)"
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Замовлення №{self.id} від {self.user.username}"

    def update_total_price(self):
        self.total_price = sum(item.total_price for item in self.items.all())
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True, blank=True)
    other = models.ForeignKey('Other', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        if self.book:
            return f"{self.book.title} - {self.quantity} шт."
        elif self.other:
            return f"{self.other.title} - {self.quantity} шт."
        return "Товар не визначено"