from django import forms

from Product.models import Product, ProductImage
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from Product.admin import ProductAdmin
from tags.models import TaggedItem


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('tag')



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0




class CustomProductAdmin(ProductAdmin):
    inlines = [ProductImageInline, TagInline]



admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)