from django.contrib import admin
from .models import Product, ShippingBox, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "length_cm", "width_cm", "height_cm", "weight_kg")

@admin.register(ShippingBox)
class ShippingBoxAdmin(admin.ModelAdmin):
    list_display = ("name", "inner_length_cm", "inner_width_cm", "inner_height_cm", "max_weight_kg", "cost")
    ordering = ("cost",)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
    inlines = [OrderItemInline]
