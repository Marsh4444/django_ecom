from django.db import models

# Create your models here.
class Cart(models.Model):
    cart_id      = models.CharField(max_length=100, blank=True)
    date_added   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cart_id}'s cart - {self.product.name} (x{self.quantity})"


class CartItem(models.Model):
    cart        = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product     = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    quantity    = models.PositiveIntegerField(default=1)
    is_active   = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.cart.cart_id}'s cart - {self.product.name} (x{self.quantity})"