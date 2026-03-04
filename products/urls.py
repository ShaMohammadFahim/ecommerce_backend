from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'items', ProductViewSet)
router.register(r'variants', ProductVariantViewSet)
router.register(r'units', UnitsViewSet)
router.register(r'colors', ProductColorViewSet)
router.register(r'sizes', ProductSizeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]