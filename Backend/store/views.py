from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer


@api_view()
def products_list(request):
    queryset = Product.objects.all().select_related('category')
    ser_data = ProductSerializer(queryset, many=True)
    return Response(ser_data.data)
    
@api_view()
def product_detail(request, id):
    
    product = get_object_or_404(Product.objects.select_related("category"), id=id)
    ser_data = ProductSerializer(product)
    return Response(ser_data.data)
    
    # try:
    #     product = get_object_or_404(Product, id=id)
    #     ser_data = ProductSerializer(product)
    #     return Response(ser_data.data)
    # except Http404 as e:
    #     return Response({"error": f"{str(e)}"})
    
    # try:
    #     product = Product.objects.get(id=id)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    
    # ser_data = ProductSerializer(product)
    # return Response(ser_data.data)