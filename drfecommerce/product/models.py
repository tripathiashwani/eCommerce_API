from django.db import models
from mptt.models import MPTTModel, TreeForeignKey



class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["parent"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

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

    def __str__(self):
        return self.name


class Productline(models.Model):
    price=models.DecimalField( max_digits=5, decimal_places=2)
    sku=models.CharField(max_length=30)
    stock_quantity=models.IntegerField()
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_line")
    is_active=models.BooleanField(default=False)