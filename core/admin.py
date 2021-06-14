from django.contrib import admin
from .models import (
    Product, 
    ExclusiveProduct, 
    ProductImage, 
    Order, 
    OrderItem, 
    Category, 
    Slider, 
    ShippingAndBilling, 
    Customer,
    NewOrderSubscriber
)


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
admin.site.register(ExclusiveProduct)
admin.site.register(NewOrderSubscriber)
