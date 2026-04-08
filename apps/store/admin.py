from django.contrib import admin
from .models import Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'modified_date', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('product_name', 'description')
    prepopulated_fields = {'slug': ('product_name',)}
