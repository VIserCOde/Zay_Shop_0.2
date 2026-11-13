from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.common.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Category Slug")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class SubCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Category Name",
                                 related_name="sub_categories")
    name = models.CharField(max_length=100, unique=True, verbose_name="Sub Category Name")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Sub Category Slug")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"


class Advertisement(BaseModel):
    """Main model for the product advertisement"""
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="advertisements",
        verbose_name="Sub Category"
    )
    title = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug (URL)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    description = models.TextField(verbose_name="Description")
    color = models.CharField(max_length=100, verbose_name="Available Colors", blank=True, null=True)
    brend = models.CharField(max_length=100, verbose_name="Brand", blank=True, null=True)
    preview = models.ImageField(upload_to="advertisements/previews/", verbose_name="Preview Image")
    stars_count = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Количество звезд (от 1 до 5)"
    )
    sizes = models.CharField(max_length=100, default="M/L/X/XL", verbose_name="Размеры")

    rating = models.FloatField(default=5.0, verbose_name="Рейтинг")

    class Meta:
        verbose_name = "Advertisement"
        verbose_name_plural = "Advertisements"

    def __str__(self):
        return self.title


class AdvertisementCharacteristic(BaseModel):
    """Model for simple product specifications (e.g., Material: Cotton)"""
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name="characteristics",
        verbose_name="Advertisement"
    )
    title = models.CharField(max_length=150, verbose_name="Property Name (e.g., Material, Weight)")
    value = models.CharField(max_length=255, verbose_name="Value (e.g., 100% Cotton, 250g)", blank=True, null=True)

    class Meta:
        verbose_name = "Advertisement Characteristic"
        verbose_name_plural = "Advertisement Characteristics"

    def __str__(self):
        return f"{self.title}: {self.value} for {self.advertisement.title}"


class AdvertisementImage(BaseModel):
    """Model for extra product images (Gallery slider)"""
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Advertisement"
    )
    image = models.ImageField(upload_to="advertisements/gallery/", verbose_name="Gallery Image")

    class Meta:
        verbose_name = "Advertisement Image"
        verbose_name_plural = "Advertisement Images"


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    advertisement = models.ForeignKey(
        'Advertisement',  # Можно указать строкой, чтобы точно не было конфликтов
        on_delete=models.CASCADE,
        verbose_name="Объявление"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'advertisement')
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return f"User ID {self.user_id} -> {self.advertisement.title}"


class Comment(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='comments',
                                      verbose_name="Товар")
    name = models.CharField(max_length=100, verbose_name="Имя автора")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveIntegerField(default=5, verbose_name="Оценка (1-5)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв покупателя"
        verbose_name_plural = "Отзывы покупателей"

    def __str__(self):
        return f"{self.name} -> {self.advertisement.title} ({self.rating}★)"


class CartItem(models.Model):
    """Модель элемента корзины"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name="Пользователь"
    )
    product = models.ForeignKey(
        'Advertisement',
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
        unique_together = ('user', 'product')  # Один товар у юзера группируется в одну строку

    def __str__(self):
        return f"{self.user.username} -> {self.product.title} ({self.quantity} шт.)"

    @property
    def total_price(self):
        """Считает общую стоимость этой позиции (Цена * Количество)"""
        return self.product.price * self.quantity


class Order(models.Model):
    """Модель самого заказа"""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('paid', 'Оплачен'),
        ('shipped', 'Доставлен'),
        ('canceled', 'Отменен'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders",
                             verbose_name="Пользователь")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адрес доставки")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая сумма")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата оформления")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.id} -> {self.user.username} (${self.total_price})"


class OrderItem(models.Model):
    """Модель товаров внутри конкретного заказа"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ")
    product = models.ForeignKey('Advertisement', on_delete=models.PROTECT, verbose_name="Товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена при покупке")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=255, verbose_name="Тема обращения")
    message = models.TextField(verbose_name="Текст сообщения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    class Meta:
        verbose_name = "Сообщение из контактов"
        verbose_name_plural = "Сообщения из контактов"
        ordering = ['-created_at']  # Сначала будут новые сообщения

    def __str__(self):
        return f"{self.name} | {self.subject}"
