from rest_framework import serializers


from .models import Product, Brand, Store, Category, SubCategory, StoreProduct, PriceHistory, ProductImage


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['id', 'name']



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
        fields = ['id', 'name', 'description', 'sku', 'main_image', 'other_images', 'brand', 'subcategory', 'created_at', 'updated_at']



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
        fields = ['id', 'brand', 'name']




class StoreProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    class Meta:
        model = StoreProduct
        fields = ['id', 'product', 'store', 'price', 'discount']




