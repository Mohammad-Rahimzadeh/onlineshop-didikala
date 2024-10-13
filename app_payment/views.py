from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from app_payment.models import BasketItem , Basket , Order , OrderItem , Transaction
from app_store.models import Product
from .forms import updateBasketItemForm

# Create your views here.


# ==================================================  basketView  ================================================= #


@login_required
def basketView(request):
    basket = Basket.objects.filter(user=request.user, is_active=True).first()
    
    if not basket:
        basket = Basket.objects.create(user=request.user)
        
    basket_items = BasketItem.objects.filter(basket=basket)

    total_price = sum(item.basket_item_total_price() for item in basket_items)
    
    total_items = sum(item.count for item in basket_items)
    
    total_score = sum(item.product.product_score() for item in basket_items)
    


    context = {
        'basket_items': basket_items ,
        'total_price': total_price ,
        'total_items':total_items ,
        'total_score':total_score ,
    }
    return render(request, 'app_payment/basket.html', context)
    



# ==================================================  addToBasketView  ================================================= #




@login_required
def addToBasketView(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    basket, created = Basket.objects.get_or_create(user=request.user, is_active=True)

    basket_item, created = BasketItem.objects.get_or_create(basket=basket, product=product)

    if created:
        basket_item.count = 1
    else:
        basket_item.count += 1

    basket_item.save()
    
    return redirect('basket_view')



# ==================================================  removeFromBasketView  ================================================= #


@login_required
def removeFromBasketView(request, item_id):
    basket_item = get_object_or_404(BasketItem, id=item_id)
    basket_item.delete()
    return redirect('basket_view')



# ==================================================  checkoutView  ================================================= #


@login_required
def checkoutView(request):
    basket, created = Basket.objects.get_or_create(user=request.user, is_active=True)
    basket_items = BasketItem.objects.filter(basket=basket)

    total_price = sum(item.basket_item_total_price() for item in basket_items)

    if request.method == 'POST':
        transaction = Transaction.objects.create(status=True, ref_code='some_unique_code', price=total_price)
        order = Order.objects.create(user=request.user, transaction=transaction)

        for item in basket_items:
            OrderItem.objects.create(order=order, product=item.product, count=item.count)

        basket.is_active = False
        basket.save()

        return redirect('order_success')

    context = {
        'basket_items': basket_items,
        'total_price': total_price ,
    }

    return render(request, 'app_payment/checkout.html', context)



# ==================================================  orderSuccessView  ================================================= #


@login_required
def orderSuccessView(request):
    return render(request, 'app_payment/order_success.html')


