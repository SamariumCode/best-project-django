from django.urls import path

from .views import product_list, product_detail

urlpatterns = [
    path('products/', product_list, name='product_list'),  # Add the name to the URL pattern
    path('products/<int:pk>/', product_detail, name='product_detail'),  # Add the name to the URL pattern
]