from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


User = get_user_model()

BLOG_STATUS = (
    ('draft' , 'پیش نویس'),
    ('published' , 'منتشر شده'),
)


class BlogCategory(models.Model):
    title = models.CharField(max_length = 50 , null=True)
    slug = models.SlugField(max_length = 50 , null=True)
    is_available = models.BooleanField(default = True)
    
    def __str__(self):
        return '{}'.format(self.title)


class Blog(models.Model):
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    category = models.ManyToManyField(BlogCategory)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255 , null=True)
    rate = models.PositiveIntegerField()
    visit_count = models.PositiveIntegerField(default=0)
    thumbnail = models.ImageField(upload_to='blog-photo/blog-thumbnail/')
    created_date = models.DateTimeField(auto_now_add=True)
    is_published = models.CharField(max_length= 10 , choices=BLOG_STATUS , blank=True, null=True)
    
    def __str__(self):
        return '{}'.format(self.title)
    
    def get_categories(self):
        return " , ".join([c.title for c in self.category.all()])  
    

class BlogContent(models.Model):
    product = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blogcontents')
    sub_title = models.CharField(max_length = 255 , blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='blog-photo/content-image/' , blank=True, null=True)
