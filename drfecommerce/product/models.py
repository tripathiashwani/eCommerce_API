from collections.abc import Collection, Iterable
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField
from django.core.exceptions import ValidationError

class ActiveQuerySet(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=True)

class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    is_active=models.BooleanField(default=False)
    objects=ActiveQuerySet().as_manager()

    class MPTTMeta:
        order_insertion_by = ["parent"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active=models.BooleanField(default=False)
    objects=ActiveQuerySet().as_manager()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug=models.SlugField(max_length=200)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_active=models.BooleanField(default=False)
    objects=ActiveQuerySet().as_manager()
    def __str__(self):
        return self.name


class Productline(models.Model):
    price=models.DecimalField( max_digits=5, decimal_places=2)
    sku=models.CharField(max_length=30)
    stock_quantity=models.IntegerField()
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_line")
    is_active=models.BooleanField(default=False)
    objects=ActiveQuerySet().as_manager()
    order=OrderField(unique_for_field="product",blank=True)
    
    def clean_fields(self,exclude=None):
        super().clean_fields(exclude=exclude)
        qs=Productline.objects.filter(product=self.product)
        for obj in qs :
            if self.id != obj.id and self.order==obj.order:
                raise ValidationError("please enter different order value")
            
    def save(self,*args,**kwargs):
        self.full_clean()
        return super(Productline,self).save(*args,**kwargs)
            
    def __str__(self):
        return str(self.sku)
    

class Product_image(models.Model):
    name = models.CharField(max_length=100)
    alternative_text=models.CharField(max_length=100)
    productline=models.ForeignKey(Productline,on_delete=models.CASCADE,related_name="product_image")
    order=OrderField(unique_for_field="product",blank=True)

    def clean_fields(self,exclude=None):
        super().clean_fields(exclude=exclude)
        qs=Product_image.objects.filter(productline=self.productline)
        for obj in qs :
            if self.id != obj.id and self.order==obj.order:
                raise ValidationError("please enter different order value")
            
    def save(self,*args,**kwargs):
        self.full_clean()
        return super(Product_image,self).save(*args,**kwargs)
    def __str__(self):
        return str(self.name)

