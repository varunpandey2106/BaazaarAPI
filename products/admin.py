from django.contrib import admin
from .models import Product, ProductImage,ProductSpecification, ProductSpecificationValue, ProductType, Category

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(ProductSpecification)
admin.site.register(ProductSpecificationValue)
admin.site.register(ProductImage)



