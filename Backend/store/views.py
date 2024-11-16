from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


@api_view(["GET", "POST"])
def products_list(request):
    if request.method == "GET":
        queryset = Product.objects.all().select_related('category')
        ser_data = ProductSerializer(queryset, many=True, context={"request": request})
        return Response(ser_data.data)
    elif request.method == "POST":
        ser_data = ProductSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response("Everything is good!")
    
@api_view()
def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related("category"), id=pk)
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