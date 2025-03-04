from django.contrib import admin
from .models import Brand, Store, Category, SubCategory, Product, StoreProduct, PriceHistory

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(SubCategory)


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'store')


    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'store', 'store__brand')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('brand', 'address', 'city')


    def get_queryset(self, request):
        return super().get_queryset(request).select_related('brand')



@admin.register(StoreProduct)
class StoreProductAdmin(admin.ModelAdmin):
    list_display = ['store', 'product', 'price', 'discount']


    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('product', 'store')





@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
