from django.shortcuts import render
from .serializers import SerpyProductSerializer, CreateProductSerializer, ProductDocumentSerializer, ProductSerializer, CategoryListSerializer
from rest_framework import filters, viewsets   
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    # CreateAPIView,
    # DestroyAPIView,
)
from .permissions import ModelViewSetsPermission
from rest_framework.exceptions import NotAcceptable
from django.utils.translation import gettext_lazy as _
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    DefaultOrderingFilterBackend,
)
from .documents import ProductDocument
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django.utils.decorators import method_decorator
from .decorators import time_calculator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.response import Response
from googletrans import Translator

translator= Translator()


# Create your views here.

#PRODUCT VIEWS
class SerpyListProductAPIView(ListAPIView):
    serializer_class = SerpyProductSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("title",)
    ordering_fields = ("created",)
    filter_fields = ("views",)
    queryset = Product.objects.all()

class ListProductView(viewsets.ModelViewSet):
    permission_classes = (ModelViewSetsPermission,)
    serializer_class = CreateProductSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("title",)
    ordering_fields = ("created",)
    filter_fields = ("views",)
    queryset = Product.objects.all()

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     print("queryset -> ", queryset)
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer)

    def update(self, request, *args, **kwargs):
        from django.contrib.auth.models import User

        if User.objects.get(username="tomas33") != self.get_object().seller:
            raise NotAcceptable(_("you don't own product"))
        return super(ListProductView, self).update(request, *args, **kwargs)


class ListProductAPIView(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("title",)
    ordering_fields = ("created",)
    filter_fields = ("views",)
    queryset = Product.objects.all()

    # def get_queryset(self):
    #     import cProfile
    #     from django.contrib.auth.models import User
    #     u = User.objects.get(id=5)
    #     p = Product.objects.create(seller=u, category=Category.objects.get(id=1), title='test', price=20, description='dsfdsfdsf', quantity=10)
    #     cProfile.runctx('for i in range(5000): ProductSerializer(p).data', globals(), locals(), sort='tottime')
    #     queryset = Product.objects.all()
    #     return queryset

    @time_calculator
    def time(self):
        return 0

    # Cache requested url for each user for 2 hours
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.time()
        return Response(serializer.data)


class ProductDocumentView(DocumentViewSet):
    document = ProductDocument
    serializer_class = ProductDocumentSerializer
    lookup_field = "id"
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    search_fields = ("title",)
    filter_fields = {"title": "title.raw"}
    ordering_fields = {"created": "created"}
    # ordering = ('-created',)
    queryset = Product.objects.all()

##CATGEORY VIEWS
class CategoryListAPIView(ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategoryListSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("name",)
    ordering_fields = ("created",)
    filter_fields = ("created",)
    # queryset = Category.objects.all()

    @time_calculator
    def time(self):
        return 0

    def get_queryset(self):
        queryset = Category.objects.all()
        self.time()
        return queryset

class CategoryAPIView(RetrieveAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {}
        for k, v in serializer.data.items():
            data[k] = translator.translate(str(v), dest="ar").text

        return Response(data)
