from django.contrib import admin
from .models import Product, Category, Brand, Productline

# Register your models here.

class ProductLineInline(admin.TabularInline):
    model=Productline

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']
    inlines=[ProductLineInline]


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Productline)
