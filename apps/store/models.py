from django.db import models
from django.urls import reverse

from apps.category.models import Category

# Create your models here.
class Product(models.Model):
    product_name    = models.CharField(max_length=255, unique=True)
    slug            = models.SlugField(max_length=255, unique=True)
    description     = models.TextField(max_length=1000, blank=True)
    price           = models.DecimalField(max_digits=10, decimal_places=2)
    stock           = models.IntegerField()
    image           = models.ImageField(upload_to='photos/products/%Y/%m/%d', blank=True, null=True)
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)

    #time stamps
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        db_table = 'products'

    def get_url(self):
        """Returns the URL to access a particular category instance."""
        return reverse('product-detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
    
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)
    

class Variation(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value    = models.CharField(max_length=100)
    is_active   = models.BooleanField(default=True)
    created_date   = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    class Meta:
        verbose_name = 'variation'
        verbose_name_plural = 'variations'
        db_table = 'variations'

    def __str__(self):
        return self.variation_value
