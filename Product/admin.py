from django.contrib import admin
from django.template.defaultfilters import title

from .models import Brand, Store, Category, SubCategory, Product, StoreProduct, PriceHistory

admin.site.register(Brand)
admin.site.register(Store)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(StoreProduct)
admin.site.register(PriceHistory)
