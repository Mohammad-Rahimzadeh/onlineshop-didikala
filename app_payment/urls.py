from django.urls import path
from app_payment import views

urlpatterns = [
    path('basket/', views.basketView, name='basket_view'),

    path('basket/add/<int:product_id>/', views.addToBasketView, name='add_to_basket'),
    path('basket/remove/<int:item_id>/', views.removeFromBasketView, name='remove_from_basket'),

    path('checkout/', views.checkoutView, name='checkout_view'),
    path('order_success/', views.orderSuccessView, name='order_success'),
    ]