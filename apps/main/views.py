from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from apps.main.models import Category, Advertisement, Favorite
from apps.main.models import Comment
from .forms import CustomRegistrationForm
from .models import ContactMessage
from .models import Order, OrderItem, CartItem


@login_required(login_url='login')
def show_contacts_page(request):
    if request.method == 'POST':
        name = request.user.username
        email = request.POST.get('email') or request.user.email
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_text
        )

        messages.success(request, f'Спасибо, {name}! Ваше сообщение успешно отправлено в службу поддержки.')
        return redirect('contact')

    return render(request, 'main/contact.html')


def show_home_page(request):
    return render(request, "main/index.html")


def show_about_page(request):
    return render(request, "main/about.html")


def show_policy_page(request):
    return render(request, "main/policy.html")


def show_shop_categories_page(request):
    categories = Category.objects.all().prefetch_related("sub_categories")
    products = Advertisement.objects.all().prefetch_related("images")
    favorite_product_ids = []
    if request.user.is_authenticated:
        favorite_product_ids = Favorite.objects.filter(user=request.user).values_list('advertisement_id', flat=True)
    return render(request, "main/shop_categories.html", locals())





@login_required
def show_favorites_page(request):
    user_favorites = Favorite.objects.filter(user=request.user).prefetch_related("advertisement__images")
    favorites = [fav.advertisement for fav in user_favorites]
    context = {"favorites": favorites}
    return render(request, "main/favorites.html", context)


@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Advertisement, id=product_id)

    Favorite.objects.get_or_create(user=request.user, advertisement=product)

    return redirect(request.META.get('HTTP_REFERER', 'shop_categories'))


@login_required
def remove_from_favorites(request, advertisement_id):
    if request.method == "POST":
        advertisement = get_object_or_404(Advertisement, id=advertisement_id)
        Favorite.objects.filter(user=request.user, advertisement=advertisement).delete()

    referer = request.META.get('HTTP_REFERER', '/favorites/')

    if 'shop/' in referer and not referer.endswith('#related'):
        return HttpResponseRedirect(f"{referer}#related")

    return HttpResponseRedirect(referer)


def show_advertisement_detail_page(request, slug):
    advertisement = get_object_or_404(
        Advertisement.objects.prefetch_related("images", "characteristics", "comments"),
        slug=slug
    )
    related_products = Advertisement.objects.exclude(id=advertisement.id).prefetch_related("images")[:4]

    favorite_product_ids = []
    cart_items = []
    total_cart_price = 0

    if request.user.is_authenticated:
        favorite_product_ids = Favorite.objects.filter(user=request.user).values_list('advertisement_id', flat=True)

        cart_items = CartItem.objects.filter(user=request.user).prefetch_related("product")

        total_cart_price = sum(item.total_price for item in cart_items)

    context = {
        "advertisement": advertisement,
        "related_products": related_products,
        "favorite_product_ids": favorite_product_ids,
        "cart_items": cart_items,
        "total_cart_price": total_cart_price,
    }
    return render(request, "main/shop_single.html", context)


@login_required
def show_cart_page(request):
    cart_items = CartItem.objects.filter(user=request.user).prefetch_related("product__images")

    total_cart_price = sum(item.total_price for item in cart_items)

    context = {
        "cart_items": cart_items,
        "total_cart_price": total_cart_price,
    }
    return render(request, "main/cart.html", context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Advertisement, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return redirect(request.META.get('HTTP_REFERER', 'shop_categories'))


@login_required
def change_cart_quantity(request, item_id, action):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

        if action == "plus":
            cart_item.quantity += 1
            cart_item.save()
        elif action == "minus":
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
            else:
                cart_item.save()

    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.delete()

    return redirect('cart')


@login_required
def checkout_page(request):
    cart_items = CartItem.objects.filter(user=request.user).prefetch_related("product")
    if not cart_items:
        return redirect('cart')

    total_cart_price = sum(item.total_price for item in cart_items)

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            total_price=total_cart_price
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
        cart_items.delete()
        return render(request, "main/order_success.html", {"order": order})

    context = {
        "cart_items": cart_items,
        "total_cart_price": total_cart_price,
    }
    return render(request, "main/checkout.html", context)


@login_required
def buy_now_instant(request, product_id):
    """Быстрая покупка при клике на Buy со страницы товара"""
    if request.method == "POST":
        product = get_object_or_404(Advertisement, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        return redirect('checkout')
    return redirect('shop_categories')


def register_view(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomRegistrationForm()
    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'main/log-in.html', {'form': form})


def logout_view(request):
    """Выход из аккаунта"""
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
    return redirect('home')


@login_required
def add_comment(request, product_id):
    """Прием отзыва только от авторизованных и динамический пересчет рейтинга товара"""
    if request.method == "POST":
        product = get_object_or_404(Advertisement, id=product_id)
        name = request.user.username
        text = request.POST.get('text')
        rating_value = int(request.POST.get('rating', 5))

        if text:
            Comment.objects.create(
                advertisement=product,
                name=name,
                text=text,
                rating=rating_value
            )
            avg_rating = product.comments.aggregate(Avg('rating'))['rating__avg']
            if avg_rating is not None:
                product.rating = round(avg_rating, 1)
                product.stars_count = int(round(avg_rating))

                product.save()  # Сохраняем изменения товара в PostgreSQL

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
