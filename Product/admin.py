from pprint import pprint
from django.contrib import admin
from .models import Brand, Store, Category, SubCategory, Product, StoreProduct, PriceHistory, ProductImage, Quantity
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from .resources import SubCategoryResource, CategoryResource, BrandResource, ProductImageResource, PriceHistoryResource, \
    StoreResource, StoreProductResource, QuantityResource, ProductResource


@admin.register(SubCategory)
class SubCategoryAdmin(ImportExportModelAdmin):
    resource_class = SubCategoryResource


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ['name', 'logo_display_readonly']
    readonly_fields = ['logo_display_readonly', ]  # добавляем поле для редактирования
    select_related = ['other_images']

    def logo_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "Нет логотипа"

    def logo_display_readonly(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" height="200" />', obj.image.url)
        return "Нет логотипа"



@admin.register(Brand)
class BrandAdmin(ImportExportModelAdmin):
    resource_class = BrandResource
    list_display = ['name', 'logo_display']
    readonly_fields = ['logo_display_readonly']  # Добавляем поле для редактирования

    def logo_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "Нет логотипа"

    def logo_display_readonly(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" height="200" />', obj.image.url)
        return "Нет логотипа"

    logo_display_readonly.short_description = 'Logo Preview'  # Название поля на странице редактирования

@admin.register(ProductImage)
class ProductImageAdmin(ImportExportModelAdmin):
    resource_class = ProductImageResource
    list_display = ['product', 'image', 'created_at']
    search_fields = ['product__name']  # Поиск по названию продукта

    # Включение дополнительных полей в редактируемой форме
    fieldsets = (
        (None, {
            'fields': ('product', 'image')
        }),
        ('Date Information', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ['created_at']


@admin.register(PriceHistory)
class PriceHistoryAdmin(ImportExportModelAdmin):
    resource_class = PriceHistoryResource
    list_display = ('product', 'store')


    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'store', 'store__brand')


@admin.register(Store)
class StoreAdmin(ImportExportModelAdmin):
    resource_class = StoreResource
    list_display = ('brand', 'address', 'city')
    search_fields = ['address']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('brand')



@admin.register(StoreProduct)
class StoreProductAdmin(ImportExportModelAdmin):
    resource_class = StoreProductResource
    list_display = ['id', 'store', 'product', 'price', 'discount']
    autocomplete_fields = ['store', 'product']

    search_fields = ['product__name', 'store__address']

    def save_model(self, request, obj, form, change):
        obj.sent = False
        obj.save()




@admin.register(Quantity)
class QuantityAdmin(ImportExportModelAdmin):
    resource_class = QuantityResource
    list_display = ['store', 'store__product', 'quantity']
    autocomplete_fields = ['store']

    def save_model(self, request, obj, form, change):
        obj.sent = False
        obj.save()

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ['name', 'logo_display_readonly']
    readonly_fields = ['logo_display_readonly', 'other_images_display_readonly']  # добавляем поле для редактирования
    select_related = ['other_images']
    search_fields = ['name']


    def logo_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "Нет логотипа"

    def logo_display_readonly(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" height="200" />', obj.image.url)
        return "Нет логотипа"

    logo_display_readonly.short_description = 'Logo Preview'


    def other_images_display_readonly(self, obj):
        images = obj.other_images.all()
        if images:
            image_html = ''.join(
                [format_html('<img src="{}" width="50" height="50" />', image.image.url) for image in images]
            )
            return format_html(image_html)
        return "Нет дополнительных изображений"

