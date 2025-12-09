from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, get_object_or_404


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title



# ====== SLIDERLAR ======
class Slide(models.Model):
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to='slides/', verbose_name='Rasm')

    def __str__(self):
        return self.title


class SlideTovar(models.Model):
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to='slide_tovar/', verbose_name='Rasm')

    def __str__(self):
        return self.title


class SlideBrand(models.Model):
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to='slide_brand/', verbose_name='Rasm')

    def __str__(self):
        return self.title


# ====== PRODUCT ======
class Products(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=20000)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='products/')
    image2 = models.ImageField(upload_to='products/')
    image3 = models.ImageField(upload_to='products/')
    image4 = models.ImageField(upload_to='products/')
    price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.title

    def snippet(self):
        return self.description[:60] + '...'

    def shortem(self):
        return self.title[:15] + '...'
    
    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum([r.rating for r in reviews]) / reviews.count(), 1)
        return 0






# ====== COMMENTS ======
class Comment(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, related_name='comments')
    comment_text = models.TextField('Comment', max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} → {self.comment_text[:25]}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


# ====== CART (SAVATCHA) ======
class CartItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.title} ({self.quantity}x)'

    def total_price(self):
        return self.product.price * self.quantity


# ====== ORDER (BUYURTMA) ======
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True)
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id}'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    total = models.IntegerField()

    def __str__(self):
        return f'{self.product.title} x{self.amount}'


# ====== REVIEW (BAHOLASH) ======
RATE_CHOICES = (
    (1, '1 - Trash'),
    (2, '2 - Bad'),
    (3, '3 - Ok'),
    (4, '4 - Good'),
    (5, '5 - Perfect'),
)

class Review(models.Model):
    product = models.ForeignKey(Products, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=0)  # 1-5 orasida
    comment_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # Foydalanuvchi bir martagina baholashi mumkin

    def __str__(self):
        return f"{self.user.username} - {self.product.title} ({self.rating})"






class Shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    work_time = models.CharField(max_length=50)
    image = models.ImageField(upload_to='shops/')

    def __str__(self):
        return self.name
    


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} -> {self.product.title}"
