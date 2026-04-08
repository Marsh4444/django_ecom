
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models  import Product
from apps.category.models import Category

# Create your views here.
def store_home(request, cat_slug=None):
    categories = None
    products = None

    if cat_slug != None:
        categories = get_object_or_404(Category, slug=cat_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True)
        product_count = products.count()


    context = {
        'products': products,
        'product_count': product_count,
    }
    
    return render(request, 'store/store.html', context)


def product_detail(request, cat_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=cat_slug, slug=product_slug)    
    except Product.DoesNotExist:
        raise Http404("Product does not exist")

    context = {
        'single_product': single_product,
    }




    return render(request, 'store/product_detail.html', context)
