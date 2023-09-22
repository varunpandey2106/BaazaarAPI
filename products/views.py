from django.shortcuts import render
from .serializers import SerpyProductSerializer, CreateProductSerializer, ProductDocumentSerializer
from rest_framework import filters, viewsets   
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from rest_framework.generics import (
    ListAPIView,
    # RetrieveAPIView,
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

# Create your views here.


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