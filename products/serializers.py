from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product, ProductViews
from drf_extra_fields.fields import Base64ImageField
import serpy 
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from drf_haystack.serializers import HaystackSerializer
from .documents import ProductDocument
from .search_indexes import ProductIndex




class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = []

class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()

    def get_category(self, obj): #custom method, determines value of category of each serialized Product instance 
        return obj.category.name #retrieves name of catgeory and returns val

    class Meta:
        model = Product
        exclude = []

class SerpyProductSerializer(serpy.Serializer):
    seller=serpy.StrField()
    Category=serpy.StrField()
    title=serpy.StrField()
    price=serpy.StrField()
    image=serpy.StrField()
    description = serpy.StrField()
    quantity = serpy.IntField()
    views = serpy.IntField()

class ProductMinSerializer(serializers.ModelSerializer): #list of products with minimal information
    class Meta:
        model=Product
        field=["title"] #show only product titles

    def to_representation(self, instance): #serializing an instance of the Product model to determine the format and content of the serialized data
        data=super().to_representation(instance)
        data= serializers.ModelSerializer.to_representation(self, instance)
        return data


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ()
        # read_only_fields = ('id', 'seller', 'category', 'title', 'price', 'image', 'description', 'quantity', 'views',)

class ProductDetailSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()
    image = Base64ImageField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Product
        exclude = ["modified"]

class ProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductViews
        exclude=["modified"]

class ProductDocumentSerializer(DocumentSerializer):
    seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.name

    class Meta(object):
        # model = Product
        document = ProductDocument
        exclude = ["modified"]

class ProductIndexSerializer(HaystackSerializer):
    class Meta:
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [ProductIndex]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes. These
        # fields belong to the search index!
        fields = ("text", "title", "category",)

class ProductViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductViews
        exclude = ["modified"]


