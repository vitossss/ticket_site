from django.contrib import admin
from .models import Ticket, Payment, Order, OrderItem


@admin.register(Ticket)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active")
    list_display_links = ("name",)
    search_fields = ("id", "name", "is_active")
    list_filter = ("creation_time",)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "time")
    list_display_links = ("user",)
    search_fields = ("id", "user")
    list_filter = ("time",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "creation_time")
    list_display_links = ("user",)
    search_fields = ("id", "user")
    list_filter = ("creation_time",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price", "discount")
    list_display_links = ("order",)
    search_fields = ("order", "product", "discount")
    list_filter = ("discount",)
