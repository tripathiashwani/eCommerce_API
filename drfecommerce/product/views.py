from django.shortcuts import render
from rest_framework import viewsets
from django.urls import reverse
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category,Brand,Product
from .serializers import CategorySerializer,BrandSerializer,ProductSerializer
from drf_spectacular.utils import extend_schema
# Create your views here.


class categoryViewSet(viewsets.ViewSet):
    queryset=Category.objects.all()
    @extend_schema(responses=CategorySerializer)
    def list(self,request):
        serializer=CategorySerializer(self.queryset,many=True)
        return Response(serializer.data)
    
class brandViewSet(viewsets.ViewSet):
    queryset=Brand.objects.all()
    @extend_schema(responses=BrandSerializer)
    def list(self,request):
        serializer=BrandSerializer(self.queryset,many=True)
        return Response(serializer.data)
    
class productViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing all products
    """
    queryset=Product.objects.all()


    lookup_field="slug"
    def retrieve(self,request,slug=None):
        """A viewset for view product by id """
        serializer=ProductSerializer(self.queryset.filter(slug=slug),many=True)
        return Response(serializer.data)
    

    @extend_schema(responses=ProductSerializer)
    def list(self,request):
        serializer=ProductSerializer(self.queryset,many=True)
        return Response(serializer.data)

    
    @action(
            methods=["get"],
            detail=False,
            url_path=r"category/(?P<category>\w+)/all",
            url_name="all"
            # url = reverse('product:Product', kwargs={'category': 'category', 'pk': 1})
    )
    def products_by_category(self,request,category=None):
        """A viewset for view product by category"""
        serializer=ProductSerializer(self.queryset.filter(category__name=category),many=True)
        return Response(serializer.data)
