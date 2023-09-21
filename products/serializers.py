from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product
from drf_extra_fields.fields import Base64ImageField




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = "modified"

class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()

    def get_category(self, obj): #custom method, determines value of category of each serialized Product instance 
        return obj.category.name #retrieves name of catgeory and returns val

    class Meta:
        model = Product
        exclude = "modified"

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("modified",)
        # read_only_fields = ('id', 'seller', 'category', 'title', 'price', 'image', 'description', 'quantity', 'views',)

class ProductDetailSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()
    image = Base64ImageField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Product
        exclude = "modified"