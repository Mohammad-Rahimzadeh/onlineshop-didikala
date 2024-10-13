from django.contrib import admin
from .models import Order , OrderItem , Basket , BasketItem , Transaction


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user' , 'transaction']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order' , 'product' , 'count']


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['__str__' , 'is_active']


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ['basket' , 'product' , 'count' , 'basket_item_total_price']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['ref_code' , 'price' , 'status']
