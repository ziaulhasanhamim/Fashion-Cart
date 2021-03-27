from django.contrib import admin
from .models import Product, ProductImage, Order, OrderItem, Category, Slider, ShippingAndBilling, Customer


class ProductImageInline(admin.StackedInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    exclude = ('sold',)
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Slider)
admin.site.register(ShippingAndBilling)
admin.site.register(Customer)
