from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product

@api_view()
def product_list(request):
    return Response("Product list")


@api_view()
def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    result = {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,

    }
    return Response(result)