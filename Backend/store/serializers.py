from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255, source="name")
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, source="price")
    inventory = serializers.IntegerField()
    
    
    
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['unit_price'] = float(representation["unit_price"])
        representation['inventory'] = float(representation["inventory"])
        return representation