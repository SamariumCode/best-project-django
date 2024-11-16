from decimal import Decimal, ROUND_DOWN
from rest_framework import serializers

from .models import Product


DOLLORS_TO_RIALS = 68000


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255, source="name")
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, source="price")
    # category = serializers.IntegerField(source="category_id")
    # category = serializers.PrimaryKeyRelatedField(
    #     queryset=Product.objects.all()
    # )
    category = serializers.StringRelatedField()
    price_after_tax = serializers.SerializerMethodField()
    inventory = serializers.IntegerField()
    price_rials = serializers.SerializerMethodField()
    
    
    def get_price_rials(self, product:Product):
        return (product.price * DOLLORS_TO_RIALS)
    
    
    def get_price_after_tax(self, product:Product):
        tax_rate = Decimal('0.35')
        price_with_tax = (product.price + (product.price * tax_rate)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        return price_with_tax
    
    
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['unit_price'] = float(representation["unit_price"])
        representation['inventory'] = int(representation["inventory"])
        return representation