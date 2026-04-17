from django.contrib import admin
from .models import Product, Variation

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'modified_date', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('product_name', 'description')
    prepopulated_fields = {'slug': ('product_name',)}


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_date')
    list_filter = ('product', 'variation_category', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('product__product_name', 'variation_value')