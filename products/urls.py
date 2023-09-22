from django.urls import path, include
from . import views, viewsets
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register(r"products", views.ProductDocumentView)
router.register(r"product-lists", views.ListProductView)
router.register(r"product-search", viewsets.ProductSearchView)


app_name="products"

urlpatterns = [
    path("serpy/product/", views.SerpyListProductAPIView.as_view()),
    path("list/product/", views.ListProductAPIView.as_view()),
    path("category/", views.CategoryListAPIView.as_view()),
    path("category/<int:pk>/", views.CategoryAPIView.as_view()),
    path("list-product/user/", views.ListUserProductAPIView.as_view()),



]
