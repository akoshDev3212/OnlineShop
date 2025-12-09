from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.store, name='store'),
    path('detail/<int:pk>/', views.products_detail, name='products_detail'),
    path('search/', views.search_result, name='search_result'),
    path('store/<int:pk>/leave-comment/', views.leave_comment, name='leave_comment'),
    path('cart/', views.cart, name='cart'),
    path('edit_cart/<int:pk>/', views.edit_cart_item, name='edit_cart_item'),
    path('delete_cart_item/<int:pk>/', views.delete_cart_item, name='delete_cart_item'),
    path('cart/create_order/', views.create_order, name='create_order'),
    path('orders/', views.orders, name='orders'),
    path('rate_product/<int:pk>/', views.rate_product, name='rate_product'),
    path('dokkonlarimiz/', views.dokkonlarimiz, name='dokkonlarimiz'),
    path('payment/', views.payment, name='payment'),
    path('category/<int:pk>/', views.category_products, name='category_products'),
    path('favorite/add/<int:pk>/', views.add_favorite, name='add_favorite'),
    path('favorite/remove/<int:pk>/', views.remove_favorite, name='remove_favorite'),
    path('favorites/', views.favorites_page, name='favorites'),
]
