from rest_framework import serializers
from .models import (
    Category, Product, ProductVariant, Units, 
    ProductImage, ProductColor, ProductSize, VariantAttributes
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = '__all__'

class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = '__all__'

class UnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = '__all__'


class VariantAttributesSerializer(serializers.ModelSerializer):
    color_name = serializers.ReadOnlyField(source='color.color_name')
    size_value = serializers.ReadOnlyField(source='size.size')

    class Meta:
        model = VariantAttributes
        fields = ['id', 'unit', 'color', 'size', 'color_name', 'size_value']

class ProductVariantSerializer(serializers.ModelSerializer):
    attributes = VariantAttributesSerializer(many=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'price', 'quantity', 'attributes']

    def create(self, validated_data):
        attributes_data = validated_data.pop('attributes', [])
        variant = ProductVariant.objects.create(**validated_data)
        for attr in attributes_data:
            VariantAttributes.objects.create(product_variant=variant, **attr)
        return variant

    def update(self, instance, validated_data):
        attributes_data = validated_data.pop('attributes', None)
        
        instance.price = validated_data.get('price', instance.price)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()

        if attributes_data is not None:
            instance.attributes.all().delete()
            for attr in attributes_data:
                VariantAttributes.objects.create(product_variant=instance, **attr)
        
        return instance

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'description', 'images', 'variants']

    def create(self, validated_data):
        variants_data = validated_data.pop('variants', [])
        product = Product.objects.create(**validated_data)
        for variant_data in variants_data:
            attrs_data = variant_data.pop('attributes', [])
            variant = ProductVariant.objects.create(product=product, **variant_data)
            for attr in attrs_data:
                VariantAttributes.objects.create(product_variant=variant, **attr)
        return product