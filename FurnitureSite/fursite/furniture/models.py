from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from djmoney.models.fields import MoneyField


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products_by_category', kwargs={"slug": self.slug})

    class Meta:
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    housing_material = models.CharField(max_length=255, verbose_name='Материал корпуса')
    facade_material = models.CharField(max_length=255, verbose_name='Материал фасада')
    housing_color = models.CharField(max_length=255, verbose_name='Цвет корпуса')
    facade_color = models.CharField(max_length=255, verbose_name='Цвет фасада')
    fittings = models.CharField(max_length=255, verbose_name='Фурнитура')
    description = models.TextField(max_length=1500, verbose_name='Описание', default='')
    price = MoneyField(decimal_places=2, default=0, default_currency='RUB', max_digits=11, verbose_name='Цена')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    favorite = models.ManyToManyField(User, related_name='favorite', blank=True, verbose_name='В избранном у')
    cart = models.ManyToManyField(User, related_name='cart', blank=True, verbose_name='В корзине у')
    Category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_product', kwargs={"slug": self.slug})

    class Meta:
        ordering = ['title']


class Image(models.Model):
    object_id = models.PositiveIntegerField(null=True, default=1)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, verbose_name='Продукт')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, default=20)
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.Product.title


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата')



