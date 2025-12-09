from django.contrib import admin
from .models import Products, Slide, Comment, CartItem, Order, OrderProduct, Review, SlideTovar, SlideBrand, Shop,Category
admin.site.register(Products)
admin.site.register(Slide)
admin.site.register(Comment)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Review)
admin.site.register(SlideTovar)
admin.site.register(SlideBrand) 
admin.site.register(Category)

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'work_time')
    search_fields = ('name', 'address')



