from django.db.models import F
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from Product.models import Product, Brand, Store, Category, SubCategory, StoreProduct, Quantity
from .serializers import ProductSerializer, BrandSerializer, StoreSerializer, CategorySerializer, SubCategorySerializer, \
    StoreProductSerializer, ActualPriceInStoreSerializer, CustomStoreProductForBasketQtyCheckSerializer


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
        'product__subcategory',

    ).prefetch_related(
        'product__other_images'
    ).annotate(
        quantity_value=F('quantity__quantity')
    ).all()
    serializer_class = StoreProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product__id', 'store__id']

    @action(methods=['get'], detail=False)
    def has_quantity(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')
        store_id = request.GET.get('store_id')

        if not product_id or not store_id:
            return Response({'error': 'No product or store_id provided'})

        try:
            product_id = int(product_id)
            store_id = int(store_id)
        except ValueError:
            return Response({'error': 'Invalid product or store id provided'}, status=status.HTTP_400_BAD_REQUEST)

        filtered_products = self.queryset.filter(product__id=product_id, store_id=store_id)

        serializer = CustomStoreProductForBasketQtyCheckSerializer(filtered_products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetPriceViewSet(ModelViewSet):
    queryset = StoreProduct.objects.all()
    serializer_class = ActualPriceInStoreSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product__id', 'store__id']


    @action(detail=False, methods=['get'])
    def bulk(self, request, pk=None):


        product_ids = request.GET.getlist('product_ids')
        store_id = request.GET.get('store_id')

        if not product_ids or not store_id:
            return Response({'error': 'No product or store_id provided'})

        try:
            product_ids = [int(i) for i in product_ids[0].split(',')]

        except ValueError:
            return Response({'error': 'Invalid product id provided'})

        filtered_products = self.queryset.filter(product__id__in=product_ids, store_id__in=store_id)

        serializer = self.get_serializer(filtered_products, many=True)


        return Response(serializer.data, status=status.HTTP_200_OK)