from import_export import resources
from import_export.fields import Field
from .models import Brand, Store, Category, SubCategory, Product, StoreProduct, PriceHistory, ProductImage, Quantity

class BrandResource(resources.ModelResource):
    class Meta:
        model = Brand

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category

class SubCategoryResource(resources.ModelResource):
    class Meta:
        model = SubCategory

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class StoreResource(resources.ModelResource):
    class Meta:
        model = Store


class StoreProductResource(resources.ModelResource):
    class Meta:
        model = StoreProduct


class PriceHistoryResource(resources.ModelResource):
    class Meta:
        model = PriceHistory

class ProductImageResource(resources.ModelResource):
    class Meta:
        model = ProductImage

class QuantityResource(resources.ModelResource):
    class Meta:
        model = Quantity
