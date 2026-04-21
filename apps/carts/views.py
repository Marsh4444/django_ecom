from django.shortcuts import get_object_or_404, redirect, render

from apps.carts.models import Cart, CartItem
from apps.store.models import Product, Variation



# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request, product_id):
    # Your add to cart logic here
    product = Product.objects.get(id=product_id)#this gets the product from the database using the provided product_id
    if request.method == 'POST':#this checks if the request method is POST, which indicates that the user has submitted a form to add the item to the cart
         product_variation = []
         for item in request.POST: #`this iterates through the POST data submitted by the user, which contains the variations of the product (e.g., color, size)    `
            key = item #this gets the key of the POST data, which represents the variation category (e.g., color, size)
            value = request.POST[key] #this gets the value of the POST data for the given key, which represents the variation value (e.g., red, large)
            
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)#this tries to get the variation that matches the product, variation category, and variation value from the database
                product_variation.append(variation)#if the variation exists, it adds it to the product_variation list
            except:
                pass#if the variation does not exist, it simply passes and does not add anything to the product_variation list
    
    #
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))#this tries to get the cart associated with the current session using a helper function _cart_id
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))#if the cart does not exist, it creates a new cart with the current session's cart_id
    cart.save()#saves the cart to the database

    # look for cart items with same product and cart
    cart_items = CartItem.objects.filter(product=product, cart=cart)

    for item in cart_items:
        existing_variations = list(item.variations.all().order_by('id'))#this gets the existing variations of the cart item and orders them by their id to ensure a consistent order for comparison
        new_variations = sorted(product_variation, key=lambda v: v.id)#this sorts the new variations by their id to ensure a consistent order for comparison

        if existing_variations == new_variations:
            item.quantity += 1
            item.save()
            return redirect('cart')

    # if no matching variation was found, create new cart item
    cart_item = CartItem.objects.create(
        product=product,
        cart=cart,
        quantity=1
    )

    if product_variation:
        cart_item.variations.add(*product_variation)#this adds the new variations to the cart item using the add method, which allows for adding multiple variations at once by unpacking the product_variation list with the * operator

    cart_item.save()

    return redirect('cart')#redirects the user to the cart page after adding the item to the cart


def remove_from_cart(request, product_id, cart_item_id):

    cart = Cart.objects.get(cart_id=_cart_id(request))#this gets the cart associated with the current session using the helper function _cart_id
    product = get_object_or_404(Product, id=product_id)#this gets the product from the database using the provided product_id, and if it does not exist, it returns a 404 error
    # get the exact cart item using its unique id
    # this avoids the "MultipleObjectsReturned" error
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)#this tries to get the specific cart item that matches the product, cart, and cart_item_id from the database
        # check if quantity is more than 1
        if cart_item.quantity > 1:
            # reduce quantity by 1
            cart_item.quantity -= 1
            cart_item.save()
        else:
            # if quantity is 1, remove the item completely
            cart_item.delete()
    except:
        pass

    # redirect back to cart page
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))#this gets the cart associated with the current session using the helper function _cart_id
    product = get_object_or_404(Product, id=product_id)#this gets the product from the database using the provided product_id, and if it does not exist, it returns a 404 error
    # get the exact cart item using its unique id
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        # delete the item completely from the cart
        cart_item.delete()

    except:
        pass

    # redirect back to cart page
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    # Your cart logic here
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))#this tries to get the cart associated with the current session using the helper function _cart_id
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)#this gets all the active cart items associated with the cart
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)#this calculates the total price of the cart by multiplying the price of each product by its quantity and adding it to the total 
            quantity += cart_item.quantity#this calculates the total quantity of items in the cart by adding the quantity of each cart item to the total quantity
        tax = (2 * total) / 100#this calculates the tax as 2% of the total price
        grand_total = total + tax#this calculates the grand total by adding the tax to the


    except Cart.DoesNotExist:
        pass# if the cart does not exist, it simply passes and does not return any cart items
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    
    return render(request, 'carts/cart.html', context)
