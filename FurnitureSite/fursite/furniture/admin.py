from django.contrib import admin
from django.contrib.admin import TabularInline
from .models import *

admin.site.register(Image)
admin.site.register(Review)


class ImageInline(TabularInline):
    extra = 1
    model = Image


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

