from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()

router.register('product', views.ProductViewSet)
router.register('category', views.CategoryViewSet)
router.register('subcategory', views.SubCategoryViewSet)
router.register('brand', views.BrandViewSet)
router.register('store', views.StoreViewSet)
router.register('storeproduct', views.StoreProductViewSet)


urlpatterns = router.urls