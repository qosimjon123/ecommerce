from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from Product.models import Product, Brand, Store, Category, SubCategory, StoreProduct
from .serializers import ProductSerializer, BrandSerializer, StoreSerializer, CategorySerializer, SubCategorySerializer, \
    StoreProductSerializer


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store__id']

class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryViewSet(ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer





class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('brand', 'subcategory')  # Оптимизация запросов
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['brand', 'subcategory']



class StoreProductViewSet(ModelViewSet):
    queryset = StoreProduct.objects.select_related('product', 'store')
    serializer_class = StoreProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'store']