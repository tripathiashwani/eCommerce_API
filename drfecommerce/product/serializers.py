from rest_framework import serializers
from .models import Product,Category,Brand,Productline

class CategorySerializer(serializers.ModelSerializer):
    category_name=serializers.CharField(source="name")
    class Meta:
        model=Category
        fields=["category_name"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields=["id","name"]

class ProductLineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Productline
        fields='__all__'

class ProductSerializer(serializers.ModelSerializer):
    brand_name=serializers.CharField(source="brand.name")
    category_name=serializers.CharField(source="category.name")
    product_line=ProductLineSerializer(many=True)
    class Meta:
        model=Product
        fields=["name","slug","description","brand_name","category_name","product_line"]

