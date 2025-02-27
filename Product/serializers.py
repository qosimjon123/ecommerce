from rest_framework import serializers

from .models import Product, Brand, Store, Category, SubCategory, StoreProduct, PriceHistory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'brand', 'subcategory', 'sku', 'name', 'description', ]




class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'brand', 'address',
                  'city', 'latitude', 'longitude',
                  'delivery_radius_km', 'is_active', ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'brand', 'name']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'category', 'name', ]

class StoreProductSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    class Meta:
        model = StoreProduct
        fields = ['id', 'product', 'store', 'price', 'discount']




