from . import models
from django.contrib import admin

from . import models
from .models import (
    CartItem, OrderItem, Favorite
)
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')


class SubCategoryAdminInline(admin.TabularInline):
    model = models.SubCategory
    extra = 1
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SubCategoryAdminInline]


class AdvertisementCharacteristicInline(admin.TabularInline):
    """Позволяет добавлять характеристики прямо на странице товара"""
    model = models.AdvertisementCharacteristic
    extra = 3


class AdvertisementImageInline(admin.TabularInline):
    """Позволяет загружать галерею картинок прямо на странице товара"""
    model = models.AdvertisementImage
    extra = 3


@admin.register(models.Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    """Регистрация модели товаров в админке"""
    list_display = ('title', 'price', 'brend', 'color', 'subcategory')
    search_fields = ('title', 'brend', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [AdvertisementCharacteristicInline, AdvertisementImageInline]


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    """Позволяет просматривать и модерировать отзывы прямо из админки"""
    list_display = ('name', 'advertisement', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'text')


class OrderItemInline(admin.TabularInline):
    """Позволяет видеть купленные товары прямо внутри карточки заказа"""
    model = models.OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity')


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    """Отображение списка заказов в админ-панели"""
    list_display = ('id', 'user', 'first_name', 'phone', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('first_name', 'phone', 'address')
    inlines = [OrderItemInline]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Позволяет видеть, какие товары пользователи добавляют в избранное"""
    list_display = ('id', 'user', 'advertisement', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'advertisement__title')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Позволяет админу видеть брошенные корзины пользователей"""
    list_display = ('id', 'user', 'product', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__title')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Отдельный список проданных позиций (для аналитики продаж)"""
    list_display = ('id', 'order', 'product', 'price', 'quantity')
    search_fields = ('product__title', 'order__id')
