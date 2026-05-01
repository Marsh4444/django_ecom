from django.db import models

# Create your models here.
class Cart(models.Model):
    cart_id      = models.CharField(max_length=100, blank=True)
    date_added   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cart_id}'s cart "


class CartItem(models.Model):
    user        = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, null=True, blank=True)
    cart        = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    variations   = models.ManyToManyField('store.Variation', blank=True)#this allows a cart item to have multiple variations (e.g., color, size) associated with it, and the blank=True argument allows for cart items that do not have any variations to be created without raising an error
    product     = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    quantity    = models.PositiveIntegerField(default=1)
    is_active   = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.product_name} (x{self.quantity}) -{self.cart.cart_id}'s cart"