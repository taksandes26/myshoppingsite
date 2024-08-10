from ..models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'category', 'slug', 'image', 'image_url', 'video', 'description', 'price', 'available',
                  'created', 'updated']
