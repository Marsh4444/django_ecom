from django.shortcuts import get_object_or_404, redirect, render

from apps.carts.models import Cart, CartItem
from apps.store.models import Product, Variation
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist



# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    # If the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')


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
        if request.user.is_authenticated:#this checks if the user is authenticated, which means they are logged in to their account
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)#if the user is authenticated, it gets all the active cart items associated with the user    
        else:#if the user is not authenticated, it gets the cart items associated with the current session's cart
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

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    # Your checkout logic here
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))#this tries to get the cart associated with the current session using the helper function _cart_id
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)#this gets all the active cart items associated with the cart
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)#this calculates the total price of the cart by multiplying the price of each product by its quantity and adding it to the total 
            quantity += cart_item.quantity#this calculates the total quantity of items in the cart by adding the quantity of each cart item to the total quantity
        tax = (2 * total) / 100#this calculates the tax as 2% of the total price
        grand_total = total + tax#this calculates the grand total by adding the tax to the total


    except Cart.DoesNotExist:
        pass# if the cart does not exist, it simply passes and does not return any cart items
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    
    return render(request, 'carts/checkout.html', context)
