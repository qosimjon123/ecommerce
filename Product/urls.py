from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()

router.register('brand', views.BrandViewSet)
router.register('brand-store', views.BrandStoreViewSet, basename='brand-store')
router.register('store', views.StoreViewSet, basename='store')
router.register('store-category', views.StoreCategoryViewSet, basename='store-category')
router.register('store-product', views.StoreProductViewSet, basename='store-product')
router.register('product', views.ProductViewSet, basename='product')


urlpatterns = router.urls