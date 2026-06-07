from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.db.models import Q
from django.http import HttpResponse, Http404 ,JsonResponse
from django.contrib.auth.decorators import login_required
from .models import (
    Products, Slide, SlideTovar, SlideBrand,
    CartItem, Order, OrderProduct, Review,
    Favorite, Category, Shop,Comment
)
from . import forms
from django.http import HttpResponseRedirect, HttpResponseForbidden

@login_required
def add_to_cart_ajax(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Products, pk=product_id)
        cart_item, created = CartItem.objects.get_or_create(customer=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

# 2. Tozalangan store funksiyasi
def store(request):
    slides = Slide.objects.all()
    slidetovars = SlideTovar.objects.all()
    slidebrands = SlideBrand.objects.all()
    products = Products.objects.all()
    categories = Category.objects.all()

    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, 'store.html', {
        'slides': slides,
        'slidetovars': slidetovars,
        'slidebrands': slidebrands,
        'products': products,
        'favorite_ids': favorite_ids,
        'categories': categories,
    })


def products_detail(request, pk):
    product = Products.objects.get(pk=pk)
    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    return render(request, 'products_detail.html', {'product': product, 'favorite_ids': favorite_ids})





@login_required
def leave_comment(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == "POST":
        Comment.objects.create(
            product=product,
            user=request.user,
            comment_text=request.POST.get('comment_text')
        )
    return redirect('store:products_detail', pk=product.pk)







def search_result(request):
    query = request.GET.get('search')
    products = Products.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ) if query else Products.objects.none()
    return render(request, 'search.html', {'products': products, 'query': query})


def cart(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


def update_cart(request):
    if request.method == "POST":
        # O'chirish tugmasi
        remove_id = request.POST.get('remove')
        if remove_id:
            CartItem.objects.filter(id=remove_id).delete()
            return redirect('store:cart')

        # Miqdorlarni yangilash
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                item_id = key.split('_')[1]
                try:
                    item = CartItem.objects.get(id=item_id)
                    qty = int(value)
                    if qty <= 0:
                        item.delete()
                    else:
                        item.quantity = qty
                        item.save()
                except CartItem.DoesNotExist:
                    continue
        return redirect('store:cart')

    return redirect('store:cart')


def edit_cart_item(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    action = request.GET.get('action')
    if action == 'take':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    else:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('store:cart')


def delete_cart_item(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return redirect('store:cart')


@login_required
def create_order(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    amount = sum(item.quantity for item in cart_items)

    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        if not address or not phone:
            return HttpResponse("Iltimos, manzil va telefon kiriting")

        order = Order.objects.create(user=request.user, address=address, phone=phone, total_price=total_price)
        for item in cart_items:
            OrderProduct.objects.create(
                order=order,
                product=item.product,
                amount=item.quantity,
                total=item.total_price(),
            )
        cart_items.delete()
        return redirect('store:store')

    return render(request, 'order_creation_page.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'amount': amount
    })


@login_required
def orders(request):
    orders_list = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders_list})


@login_required
def rate_product(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == "POST":
        rating = int(request.POST.get("rating", 0))
        if 1 <= rating <= 5:
            review, created = Review.objects.get_or_create(user=request.user, product=product)
            review.rating = rating
            review.save()
    return redirect('store:products_detail', pk=product.pk)


def dokkonlarimiz(request):
    shops = Shop.objects.all()
    return render(request, 'dokkonlarimiz.html', {'shops': shops})


def payment(request):
    return render(request, 'payment.html')


def category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Products.objects.filter(category=category, id__isnull=False)
    return render(request, 'category_products.html', {'category': category, 'products': products})


@login_required
def add_favorite(request, pk):
    product = get_object_or_404(Products, pk=pk)
    Favorite.objects.get_or_create(user=request.user, product=product)
    return redirect(request.META.get("HTTP_REFERER", "store:store"))


@login_required
def remove_favorite(request, pk):
    fav = get_object_or_404(Favorite, pk=pk, user=request.user)
    fav.delete()
    return redirect(request.META.get("HTTP_REFERER", "store:favorites_page"))


@login_required
def favorites_page(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("product")
    return render(request, "favorites.html", {"favorites": favorites})


