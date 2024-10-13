from django.db import models
from django.contrib.auth import get_user_model
from app_store.models import Product

# Create your models here.


User = get_user_model()

TRANSACTION_STATUS_CHOICES = (
    (False , 'ناموفق'),
    (True , 'موفق')
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.OneToOneField('Transaction', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.user , self.transaction)




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    def __str__(self):
        return '{} - {}'.format(self.product , self.count)




class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add = True , blank = True , null = True)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return '{} {}'.format(self.user.first_name , self.user.last_name)



class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name='basket_products')
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{} - {} - {}'.format(self.basket , self.product , self.count)
    
    def basket_item_total_price(self):
        return self.product.get_final_price() * self.count
    
    def total_basket_count(self):
        return self.count


class Transaction(models.Model):
    status = models.BooleanField(default=False, choices=TRANSACTION_STATUS_CHOICES)
    ref_code = models.CharField(max_length=255)
    price = models.PositiveIntegerField()

    def __str__(self):
        return '{} - {} - {}'.format(self.ref_code , self.price , self.status)