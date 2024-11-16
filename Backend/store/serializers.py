from decimal import Decimal, ROUND_DOWN
from rest_framework import serializers

from .models import Product, Category


DOLLORS_TO_RIALS = 68000


class CategorySerializer(serializers.ModelSerializer):
    # title = serializers.CharField(max_length=255)
    # description = serializers.CharField(max_length=255)    
    class Meta:
        model = Category
        fields = ["id", "title", "description"]

class ProductSerializer(serializers.ModelSerializer):
    
    unit_price = serializers.IntegerField(source="price")
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name="category_detail",
    )
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    price_after_tax = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "category", "unit_price", "inventory", "price_after_tax"]
        
    def get_price_after_tax(self, product:Product):
        tax_rate = Decimal('0.35')
        price_with_tax = (product.price + (product.price * tax_rate)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        return price_with_tax
    
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['unit_price'] = float(representation["unit_price"])
        representation['inventory'] = int(representation["inventory"])
        return representation
    