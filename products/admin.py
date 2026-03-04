from django.contrib import admin
from .models import Product, ProductVariant, Category, VariantAttributes, ProductColor, ProductSize, Units

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductColor)
admin.site.register(ProductSize)
admin.site.register(Units)

class VariantAttributesInline(admin.TabularInline):
    model = VariantAttributes
    extra = 1 

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'price', 'quantity', 'display_attributes')
    inlines = [VariantAttributesInline]

    def display_attributes(self, obj):
        return ", ".join([f"{a.color.color_name if a.color else ''} {a.size.size if a.size else ''}".strip() 
                         for a in obj.attributes.all()])
    display_attributes.short_description = 'Attributes'