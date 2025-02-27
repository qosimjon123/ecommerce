from rest_framework.viewsets import ModelViewSet
from Product.models import Product, Brand, Store, Category, SubCategory, StoreProduct
from .serializers import ProductSerializer, BrandSerializer, StoreSerializer, CategorySerializer, SubCategorySerializer, \
    StoreProductSerializer


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


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
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class StoreProductViewSet(ModelViewSet):
    queryset = StoreProduct.objects.all()
    serializer_class = StoreProductSerializer