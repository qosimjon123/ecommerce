from django_filters import rest_framework as filters
from django.db.models import F, Prefetch
from django.db import models
from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, mixins
from Product.models import Product, Brand, Store, Category, SubCategory, ProductVariant, Inventory, Schedule, Unit
from .serializers import ProductSerializer, BrandSerializer, BrandStoreSerializer, StoreSerializer, CategorySerializer, SubCategorySerializer, \
    ProductVariantSerializer, InventorySerializer, ScheduleSerializer, UnitSerializer, StoreCategorySerializer, StoreCatalogSerializer, OptimizedProductSerializer, MinimalProductSerializer
from .pagination import CustomPagination


class BrandViewSet(ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend]



class BrandStoreViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Brand.objects.prefetch_related('stores').all()
    serializer_class = BrandStoreSerializer
    filter_backends = [DjangoFilterBackend]


class StoreViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    pagination_class = None  # Disable pagination


class StoreCategoryViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Store.objects.prefetch_related('categories__subcategories').all()
    serializer_class = StoreCategorySerializer
    filter_backends = [DjangoFilterBackend]
    


class StoreProductViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreCatalogSerializer  # Сериализатор, который возвращает магазин и продукты
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'products__variants__barcode',
        'products__sub_category'
    ]
    
    def get_queryset(self):
        """Переопределяем queryset для правильной фильтрации вариантов по barcode"""
        queryset = super().get_queryset()
        
        # Получаем barcode из параметров запроса
        barcode = self.request.query_params.get('products__variants__barcode')
        
        if barcode:
            # Фильтруем магазины по продуктам с нужным barcode
            queryset = queryset.filter(products__variants__barcode=barcode)
            
            # Используем Prefetch для фильтрации вариантов только с нужным barcode
            filtered_variants = Prefetch(
                'products__variants',
                queryset=ProductVariant.objects.filter(barcode=barcode).prefetch_related('inventories')
            )
            queryset = queryset.prefetch_related(
                Prefetch('products', queryset=Product.objects.prefetch_related(filtered_variants)),
                'products__product_images',
                'products__unit'
            )
        else:
            # Если barcode не указан, используем обычный prefetch
            queryset = queryset.prefetch_related(
                'products__variants__inventories',
                'products__product_images',
                'products__unit'
            )
        
        return queryset


class ProductViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['store__id', 'sub_category__id', 'variants__barcode']
    ordering_fields = ['max_quantity']
    ordering = ['-max_quantity']  # сортировка по остаткам по умолчанию
    
    def get_queryset(self):
        """Переопределяем queryset для правильной сортировки по остаткам"""
        queryset = super().get_queryset()
        
        # Получаем barcode из параметров запроса
        barcode = self.request.query_params.get('variants__barcode')
        
        if barcode:
            # Фильтруем продукты по barcode
            queryset = queryset.filter(variants__barcode=barcode)
            
            # Используем Prefetch для фильтрации вариантов только с нужным barcode
            filtered_variants = Prefetch(
                'variants',
                queryset=ProductVariant.objects.filter(barcode=barcode).prefetch_related('inventories')
            )
            queryset = queryset.prefetch_related(
                filtered_variants,
                'product_images',
                'unit'
            )
        else:
            # Если barcode не указан, используем обычный prefetch
            queryset = queryset.prefetch_related(
                'variants__inventories',
                'product_images',
                'unit'
            )

        # Всегда добавляем аннотацию для сортировки по остаткам
        queryset = queryset.annotate(
            max_quantity=models.Max('variants__inventories__quantity')
        )
        
        # Если запрошена сортировка по остаткам
        ordering = self.request.query_params.get('ordering', '')
        if 'max_quantity' in ordering:
            if ordering.startswith('-'):
                queryset = queryset.order_by('-max_quantity')
            else:
                queryset = queryset.order_by('max_quantity')
        
        return queryset