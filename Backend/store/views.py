from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


@api_view()
def products_list(request):
    queryset = Product.objects.all().select_related('category')
    ser_data = ProductSerializer(queryset, many=True, context={"request": request})
    return Response(ser_data.data)
    
@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product.objects.select_related("category"), id=id)
    ser_data = ProductSerializer(product, context={"request": request})
    return Response(ser_data.data)


@api_view()
def category_list(request):
    queryset = Category.objects.all().prefetch_related('products')
    ser_data = CategorySerializer(queryset, many=True, context={"request":request})
    return Response(ser_data.data)

@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, id=pk)
    ser_data = CategorySerializer(category, context={"request":request})
    return Response(ser_data.data)