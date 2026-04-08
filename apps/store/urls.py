from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.store_home, name='store-home'),
    path('<slug:cat_slug>/', views.store_home, name='store-category'),
    path('<slug:cat_slug>/<slug:product_slug>/', views.product_detail, name='product-detail'),

]