
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from apps.carts.models import CartItem
from apps.carts.views import _cart_id
from .models  import Product
from apps.category.models import Category

from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q

# Create your views here.
def store_home(request, cat_slug=None):
    categories = None
    products = None

    if cat_slug != None:
        categories = get_object_or_404(Category, slug=cat_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 1)   
        page = request.GET.get('page')
        products = paginator.get_page(page)
        product_count = Product.objects.filter(category=categories, is_available=True).count()
    else:
        products = Product.objects.all().filter(is_available=True)
        paginator = Paginator(products, 6)   
        page = request.GET.get('page')
        products = paginator.get_page(page)
        product_count = Product.objects.all().filter(is_available=True).count()


    context = {
        'products': products,
        'product_count': product_count,
    }
    
    return render(request, 'store/store.html', context)


def product_detail(request, cat_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=cat_slug, slug=product_slug)    
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists() 
#this checks if the product is already in the cart for the current session by filtering the CartItem model based on the cart_id and product. It returns True if the product is in the cart, and False otherwise.
    
    except Product.DoesNotExist:
        raise Http404("Product does not exist")

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }

    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword)) 
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
        'keyword': keyword
    }
    return render(request, 'store/store.html', context)
