from django.db import models
from app_store.models import Product
from django.contrib.auth import get_user_model

# Create your models here.


User = get_user_model()

GET_NEWSLETTER_STATUS = (
    ('بله' , 'بله'),
    ('خیر' , 'خیر')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True , related_name='profile')
    phone_number = models.CharField(max_length=20)
    natural_id = models.CharField(max_length=50)
    card_no = models.CharField(max_length=16)
    get_newsletter = models.CharField(max_length=3, choices=GET_NEWSLETTER_STATUS, null=True)
    image = models.ImageField(upload_to='profile-photo/' , null=True)
    user_score = models.PositiveIntegerField(editable=False , default=10)
    
    def __str__(self):
        return '{} {}'.format(self.user.first_name , self.user.last_name)




class Address(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True , related_name='addresses')
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return '{}'.format(self.profile)
    
    
    
    
class Favorite(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    
    def __str__(self):
        return '{}'.format(self.user.username)
    


class FavoriteProduct(models.Model):
    favorite = models.ForeignKey(Favorite , on_delete=models.CASCADE , related_name='favorite_products')
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    
    def __str__(self):
        return '{} - {}'.format(self.favorite , self.product.name_fa)