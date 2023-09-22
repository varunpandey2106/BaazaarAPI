from django.shortcuts import render
from .serializers import SerpyProductSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from rest_framework.generics import (
    ListAPIView,
    # RetrieveAPIView,
    # CreateAPIView,
    # DestroyAPIView,
)

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
