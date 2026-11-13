from django.urls import path

from . import views

urlpatterns = [
    path('', views.show_home_page, name='home'),
    path('about/', views.show_about_page, name='about'),
    path('contact/', views.show_contacts_page, name='contact'),
    path('policy/', views.show_policy_page, name='policy'),
    path('shop/', views.show_shop_categories_page, name='shop_categories'),
    path('shop/<slug:slug>/', views.show_advertisement_detail_page, name='shop_single'),
    path('cart/', views.show_cart_page, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/quantity/<int:item_id>/<str:action>/', views.change_cart_quantity, name='change_cart_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_page, name='checkout'),
    path('buy-now/<uuid:product_id>/', views.buy_now_instant, name='buy_now_instant'),

    path('shop/comment/add/<uuid:product_id>/', views.add_comment, name='add_comment'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('favorites/add/<uuid:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<uuid:advertisement_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('cart/add/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('favorites/', views.show_favorites_page, name='favorites_page'),

]
