from rest_framework import viewsets
from .models import *
from .serializers import *
from .permissions import IsAdminUserRole # Shobar upore import hobe

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserRole]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUserRole]

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAdminUserRole]

class ProductColorViewSet(viewsets.ModelViewSet):
    queryset = ProductColor.objects.all()
    serializer_class = ProductColorSerializer
    permission_classes = [IsAdminUserRole]

class ProductSizeViewSet(viewsets.ModelViewSet):
    queryset = ProductSize.objects.all()
    serializer_class = ProductSizeSerializer
    permission_classes = [IsAdminUserRole]

class UnitsViewSet(viewsets.ModelViewSet):
    queryset = Units.objects.all()
    serializer_class = UnitsSerializer
    permission_classes = [IsAdminUserRole]