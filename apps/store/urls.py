from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.store_home, name='store-home'),
    path('category/<slug:cat_slug>/', views.store_home, name='store-category'),
    path('category/<slug:cat_slug>/<slug:product_slug>/', views.product_detail, name='product-detail'),
    path('search/', views.search, name='search'),
]