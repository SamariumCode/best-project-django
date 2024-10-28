from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import *

from .models import *

def home(request):
    
    # orders = OrderItem.objects.all().select_related('order__customer').select_related('product__category')
    products = Product.objects.annotate(comments_count=Count("comments"))
    list_product = list(products)
    
    return render(request, 'store/index.html', {'products': list_product})
