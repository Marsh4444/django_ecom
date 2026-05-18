import datetime

from django.shortcuts import redirect, render
from apps.orders.models import Order
from apps.carts.models import CartItem
from .forms import OrderForm

# Create your views here.
def payments(request):
    """View to handle payment processing."""
    return render(request, 'orders/payment.html')


def place_order(request, total=0, quantity=0):
    """View to place an order based on the items in the cart."""

    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total = (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax
     
    if request.method == 'POST':
        # Here you would typically handle the order placement logic,
        # such as creating an Order object, processing payment, etc.
        # For now, we'll just redirect to a success page or the store.
        form = OrderForm(request.POST)
        if form.is_valid():
            # Process the order here (e.g., create Order object, save to database)
            # For example:
            # order = form.save(commit=False)
            # order.user = current_user
            # order.save()
            # You might also want to clear the cart after placing the order
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone_number = form.cleaned_data['phone_number']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.orders_note = form.cleaned_data['orders_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR') # Get the client's IP address
            data.save()

            #to generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20240617
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            return redirect('checkout')  # Redirect to a success page after placing the order
        return redirect('checkout')  # Redirect back to the checkout page if the form is invalid


    return render(request, 'orders/place_order.html')
