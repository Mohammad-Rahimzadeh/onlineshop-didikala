from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from app_blog.models import Blog

# Create your models here.

User = get_user_model()

POINT_TYPE_STATUS = (
    (True , 'نقاط قوت') , 
    (False , 'نقاط ضعف')
)

class Comment(models.Model):
    product = models.ForeignKey('app_store.Product', on_delete=models.CASCADE , related_name='products_comment' , blank=True, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE , related_name='blogs_comment' , blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True , related_name='user_comments')
    title = models.CharField(max_length=255 ,blank=True, null=True)
    body = models.TextField()
    strength = models.TextField(blank=True, null=True)
    weakness = models.TextField(blank=True, null=True)
    rate = models.PositiveIntegerField(blank=True, null=True)
    is_suggest = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return '{} - {}'.format(self.title , self.product)

# class Point(models.Model):
#     """ 
#     نقاط ضعف و قوت 
    
#     """
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE , related_name='comment_point' , blank=True, null=True)
    
#     def __str__(self):
#         return '{}'.format(self.comment)
    

class IsUsefull(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)     
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_useful = models.BooleanField(blank=True, null=True)
    
    def __str__(self):
        return '{} - {}'.format(self.comment , self.is_useful)
    
    
class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")
    