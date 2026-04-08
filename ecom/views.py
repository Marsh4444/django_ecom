from django.shortcuts import get_object_or_404, render


from apps.store.models import Product

def home(request):
    products = Product.objects.filter(is_available=True).order_by('-created_date')


    context = {
        'products': products,
    }   

    return render(request, 'home.html', context)