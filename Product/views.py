from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from Product.models import Product, Brand, Store, Category, SubCategory, StoreProduct, Quantity
from .serializers import ProductSerializer, BrandSerializer, StoreSerializer, CategorySerializer, SubCategorySerializer, \
    StoreProductSerializer, ActualPriceInStoreSerializer


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store__id']

class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.select_related('brand').all()
    serializer_class = CategorySerializer


class SubCategoryViewSet(ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('brand', 'subcategory').prefetch_related('other_images')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['brand', 'subcategory']


class StoreProductViewSet(ModelViewSet):
    queryset = StoreProduct.objects.select_related(
        'store__brand',  # Загружаем Store и связанный Brand
        'product__brand',  # Загружаем Product и связанный Brand
        'product__subcategory'  # Загружаем SubCategory и Category
    ).prefetch_related(
        'product__other_images'  # Загружаем связанные ProductImage, если используются
    ).all()
    serializer_class = StoreProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product__id', 'store__id']




class GetPriceViewSet(ModelViewSet):
    queryset = StoreProduct.objects.all()
    serializer_class = ActualPriceInStoreSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product__id', 'store__id']
