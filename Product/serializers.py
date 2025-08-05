from rest_framework import serializers
from rest_framework.utils import representation

from .models import Product, Brand, Store, Category, SubCategory, PriceHistory, ProductImage, Schedule, Unit, ProductVariant, Inventory


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title', 'image', 'is_only_warehouse', 'created_at', 'updated_at']


class OptimizedBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title', 'image', 'is_only_warehouse', 'created_at', 'updated_at']


class StoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Store
        fields = [
            'id', 'brand', 'address', 'city', 'latitude', 'longitude',
            'delivery_radius_km', 'is_active', 'created_at', 'updated_at', 'is_only_warehouse'
        ]


class OptimizedStoreSerializer(serializers.ModelSerializer):
    brand = OptimizedBrandSerializer(read_only=True)
    
    class Meta:
        model = Store
        fields = [
            'id', 'brand', 'address', 'city', 'latitude', 'longitude',
            'delivery_radius_km', 'is_active', 'created_at', 'updated_at', 'is_only_warehouse'
        ]


class BrandStoreSerializer(serializers.ModelSerializer):
    stores = StoreSerializer(many=True)
    
    class Meta:
        model = Brand
        fields = ['id', 'title', 'image', 'is_only_warehouse', 'created_at', 'updated_at', 'stores']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'category', 'title', 'image_url']




class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True)
    class Meta:
        model = Category
        fields = [
            'id', 'title', 'description', 'created_at', 'updated_at', 'image', 'store', 'subcategories'
        ]


class OptimizedCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'title', 'description', 'created_at', 'updated_at', 'image', 'store'
        ]




class OptimizedSubCategorySerializer(serializers.ModelSerializer):
    category = OptimizedCategorySerializer(read_only=True)
    
    class Meta:
        model = SubCategory
        fields = ['id', 'category', 'title', 'image_url']


class StoreCategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Store
        fields = ['id', 'address', 'city', 'created_at', 'updated_at', 'categories']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'order', 'alt_text', 'created_at']


class InventorySerializer(serializers.ModelSerializer):    
    class Meta:
        model = Inventory
        fields = ['quantity']


class ProductVariantSerializer(serializers.ModelSerializer):
    inventories = InventorySerializer(many=True)
    
    class Meta:
        model = ProductVariant
        fields = ['id', 'price', 'discount', 'variant_value', 'variant_attributes', 'height', 'width', 'depth', 'barcode', 'weight', 'inventories']

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'title', 'short_name']


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)
    product_images = ProductImageSerializer(many=True)
    unit = UnitSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'options', 'internal_sku', 'image',
            'group_id', 'sub_category', 'store', 'unit', 'age_restriction', 'product_images', 'variants'
        ]

class OptimizedProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    variants = ProductVariantSerializer(many=True)
    unit = UnitSerializer(read_only=True)
    sub_category = OptimizedSubCategorySerializer(read_only=True)
    store = OptimizedStoreSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'options', 'internal_sku', 'image',
            'group_id', 'sub_category', 'store', 'unit', 'age_restriction', 'product_images', 'variants'
        ]



class StoreCatalogSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['id', 'address', 'products']

    def get_products(self, obj):
        request = self.context.get('request')
        barcode = request.query_params.get('products__variants__barcode') if request else None
        sub_category = request.query_params.get('products__sub_category') if request else None
        products = obj.products.all()
        if barcode:
            products = products.filter(variants__barcode=barcode)
            # Используем Prefetch для фильтрации вариантов только с нужным barcode
            from django.db.models import Prefetch
            filtered_variants = Prefetch(
                'variants',
                queryset=ProductVariant.objects.filter(barcode=barcode).prefetch_related('inventories')
            )
            products = products.prefetch_related(
                filtered_variants,
                'product_images',
                'unit'
            )
        else:
            # Если barcode не указан, используем обычный prefetch
            products = products.prefetch_related('variants__inventories', 'product_images', 'unit')
        # ВАЖНО: передаём context!
        return ProductSerializer(products, many=True, context=self.context).data



class ScheduleSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)
    
    class Meta:
        model = Schedule
        fields = ['id', 'store', 'schedule_type', 'weekday', 'is_working', 'open_time', 'close_time', 'is_retail_open', 'is_delivery_available', 'is_warehouse_open']




class PriceHistorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    
    class Meta:
        model = PriceHistory
        fields = ['id', 'product', 'store', 'old_price', 'new_price', 'old_discount', 'new_discount', 'changed_at']










class StoreProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    quantity = serializers.IntegerField(source='quantity_value')


    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'store', 'price', 'discount', 'quantity']




class CustomStoreProductForBasketQtyCheckSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    quantity = serializers.IntegerField(source='quantity_value')


    class Meta:
        model = ProductVariant
        fields = ['product', 'store', 'quantity']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if 'store' in representation:
            store_data = representation['store']
            allowed_fields = ['id']
            store_data = {key: store_data[key] for key in store_data if key in allowed_fields }
            representation['store'] = store_data

        if 'product' in representation:
            product_data = representation['product']
            allowed_fields = ['id']
            product_data = {key: product_data[key] for key in product_data if key in allowed_fields}
            representation['product'] = product_data





        return representation


class ActualPriceInStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['price', 'discount', 'product_id', 'store_id']


class MinimalProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    variants = ProductVariantSerializer(many=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'options', 'internal_sku', 'image',
            'group_id', 'sub_category_id', 'store_id', 'unit_id', 'age_restriction', 
            'product_images', 'variants'
        ]
