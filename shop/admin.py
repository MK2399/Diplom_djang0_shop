from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 5
    list_filter = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price',
        'available',
        'category',
        'slug',
    ]
    list_display_links = ['name',]
    list_editable = ['category', 'available', 'price']
    list_filter = ['category', 'available']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 5
    search_fields = ['name', 'price']
    ordering = ['price']