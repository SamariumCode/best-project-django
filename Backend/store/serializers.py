from decimal import Decimal, ROUND_DOWN
from django.utils.text import slugify
from rest_framework import serializers

from .models import Product, Category, Discount


DOLLORS_TO_RIALS = 68000

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description']

    # def create(self, validated_data):
    #     category = Category.objects.create(**validated_data)
    #     return category
    
    

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'discount', 'description']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    discounts = DiscountSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'description', 'price', 'inventory', 'discounts']

    def create(self, validated_data):
        category_data = validated_data.pop('category', None)
        if category_data:
            category, created = Category.objects.get_or_create(**category_data)
        
        discounts_data = validated_data.pop('discounts', [])
        discounts = []
        for discount_data in discounts_data:
            discount, created = Discount.objects.get_or_create(**discount_data)
            discounts.append(discount)

        product = Product.objects.create(category=category, **validated_data)
        
        if discounts:
            product.discounts.set(discounts)

        return product
