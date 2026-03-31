from django.db import models

# Create your models here.
class Category(models.Model):
    """Model representing a category for products."""
    cat_name = models.CharField(max_length=55, unique=True)
    slug = models.SlugField(unique=True , max_length=100)
    cat_image = models.ImageField(upload_to='media/category_images/%Y/%m/%d', blank=True, null=True)
    description = models.TextField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.cat_name
