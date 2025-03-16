from rest_framework import serializers
from rest_framework.utils import representation

from .models import Product, Brand, Store, Category, SubCategory, StoreProduct, PriceHistory, ProductImage, Quantity


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['id', 'name', 'image']



class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'category', 'name', ]




class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()  # Показывает название бренда
    subcategory = serializers.StringRelatedField()  # Показывает название подкатегории
    other_images = ProductImageSerializer(many=True, read_only=True)  # Список доп. картинок

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'sku', 'image', 'other_images', 'brand', 'subcategory', 'created_at', 'updated_at']



class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'brand', 'address',
                  'city', 'latitude', 'longitude',
                  'delivery_radius_km', 'is_active', ]

class CategorySerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'brand', 'name', 'image']








class StoreProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    quantity = serializers.IntegerField(source='quantity_value')


    class Meta:
        model = StoreProduct
        fields = ['id', 'product', 'store', 'price', 'discount', 'quantity']




class CustomStoreProductForBasketQtyCheckSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    quantity = serializers.IntegerField(source='quantity_value')


    class Meta:
        model = StoreProduct
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
        model = StoreProduct
        fields = ['price', 'discount', 'product_id', 'store_id']