from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self): return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    def __str__(self): return self.name

# Ei model-ti miss houay error ashchilo
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

class ProductColor(models.Model):
    color_name = models.CharField(max_length=100)
    def __str__(self): return self.color_name

class ProductSize(models.Model):
    size = models.CharField(max_length=50)
    def __str__(self): return self.size

class Units(models.Model):
    unit_type = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    def __str__(self): return f"{self.unit_type} - {self.value}"

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    def __str__(self): return f"{self.product.name} - {self.price}"

class VariantAttributes(models.Model):
    product_variant = models.ForeignKey(ProductVariant, related_name='attributes', on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, null=True, blank=True)
    unit = models.ForeignKey(Units, on_delete=models.CASCADE, null=True, blank=True)