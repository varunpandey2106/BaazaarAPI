from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product



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