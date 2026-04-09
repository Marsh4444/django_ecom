from django.shortcuts import redirect, render

from apps.carts.models import Cart, CartItem
from apps.store.models import Product

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request, product_id):
    # Your add to cart logic here
    product = Product.objects.get(id=product_id)#this gets the product from the database using the provided product_id
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))#this tries to get the cart associated with the current session using a helper function _cart_id
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))#if the cart does not exist, it creates a new cart with the current session's cart_id
    cart.save()#saves the cart to the database

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)#this tries to get the cart item that matches the product and cart
        cart_item.quantity += 1#if the cart item exists, it increments the quantity by 1
        cart_item.save()#saves the updated cart item to the database
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)#if the cart item does not exist, it creates a new cart item with the product, cart, and a quantity of 1
        cart_item.save()#saves the new cart item to the database


    return redirect('cart')#redirects the user to the cart page after adding the item to the cart

def cart(request, total=0, quantity=0, cart_items=None):
    # Your cart logic here
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))#this tries to get the cart associated with the current session using the helper function _cart_id
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)#this gets all the active cart items associated with the cart
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)#this calculates the total price of the cart by multiplying the price of each product by its quantity and adding it to the total 
            quantity += cart_item.quantity#this calculates the total quantity of items in the cart by adding the quantity of each cart item to the total quantity
    
    except Cart.DoesNotExist:
        pass# if the cart does not exist, it simply passes and does not return any cart items
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    
    return render(request, 'carts/cart.html', context)
