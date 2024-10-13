from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator , MaxValueValidator
from django.utils.html import format_html
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

# Create your models here.


User = get_user_model()

WRITTEN_LANGUAGE_CHOICES = (
    ('persian' , 'فارسی'),
    ('english' , 'انگلیسی')
)

COLOR_CHOICES = (
    ('مشکی' , 'مشکی'),
    ('سفید' , 'سفید'),
    ('نقره ای' , 'نقره ای'),
    ('طلایی' , 'طلایی'),
    ('سبز' , 'سبز'),
    ('قرمز' , 'قرمز'),
    ('آبی' , 'آبی'),
)


CLOTHES_SIZE_CHOICES = (
    ('S' , 'S'),
    ('M' , 'M'),
    ('L' , 'L'),
    ('XL' , 'XL'),
)


# ============================================================================================================= #
# ==================================================== Category =============================================== #
# ============================================================================================================= #



class Category(models.Model):
    parent = models.ForeignKey( 'self', related_name='sub_categories', on_delete=models.SET_NULL, null=True , blank=True)
    name = models.CharField(max_length = 50 , null=True)
    slug = models.SlugField(max_length = 50 , null=True)
    image = models.ImageField(upload_to = 'parent-category-photo' , null=True , blank=True)
    is_available = models.BooleanField(default = True)
    
    def __str__(self):
        return '{}'.format(self.name)



# ============================================================================================================= #
# ==================================================== BaseProduct ============================================ #
# ============================================================================================================= #



class Product(models.Model):
    seller = models.CharField(max_length=255 , default='Didikala')
    category = models.ManyToManyField(Category)
    name_fa = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255 , blank=True, null=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE , null=True , blank=True)
    model = models.CharField(max_length=255, null=True , blank=True)
    price = models.PositiveIntegerField()
    off_percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)] , null=True)
    count = models.PositiveIntegerField()
    review = models.TextField(blank=True, null=True)
    rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, null=True)
    Warranty_period = models.PositiveIntegerField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    is_suggested = models.BooleanField(default=False)
    visit_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return '{}'.format(self.name_fa)
    
    @property
    def images(self):
        return Image.objects.filter( object_id=self.id, content_type=ContentType.objects.get_for_model(self.__class__).id )
    
    def get_absolute_url(self):
        return reverse('app_store:product_detail', args=(self.id, ))
    
    def get_categories(self):
        return " , ".join([c.name for c in self.category.all()])    
    
    def create_product_code(self):
        category_ids = [c.id for c in self.category.filter(parent__isnull=True)]
        product_code = str((category_ids[0] + self.id + 100))
        return product_code
    
    def get_final_price(self):
        final_price = (self.price * (100 - self.off_percent)) / 100
        return final_price
    
    def get_reduce_price(self):
        final_price = (self.price * (100 - self.off_percent)) / 100
        reduce_price = self.price - final_price
        return reduce_price
    
    def product_score(self):
        if 0 < self.price <= 500000:
            point = 10
        elif 500000 < self.price <= 1000000:
            point = 15
        elif 1000000 < self.price <= 10000000:
            point = 20
        elif 10000000 < self.price <= 50000000:
            point = 25
        elif 50000000 < self.price <= 100000000:
            point = 30
        elif 100000000 < self.price:
            point = 40
                 
        return point

    def is_clothing(self):
        return self.category.filter(name='مد و پوشاک').exists()
    


# ============================================================================================================= #    
# ==================================================== Color ================================================== #
# ============================================================================================================= #



class Color(models.Model):
    product = models.ManyToManyField(Product , blank=True , related_name='product_color')
    color_name = models.CharField(max_length=255, choices=COLOR_CHOICES , null=True , blank=True)

    def __str__(self):
        return '{} - {}'.format(self.product , self.color_name)
    
    def get_products(self):
        return " , ".join([p.name_fa for p in self.product.all()])
    


# ============================================================================================================= #    
# ==================================================== Size =================================================== #
# ============================================================================================================= #



class Size(models.Model):
    product = models.ManyToManyField(Product)
    size = models.CharField(max_length=50, choices=CLOTHES_SIZE_CHOICES , blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.product , self.size)
    
    def get_products(self):
        return " , ".join([p.title for p in self.product.all()])
    
    def save(self, *args, **kwargs):
        for product in self.product.all():
            if not product.is_clothing():
                raise ValueError("امکان تعریف سایز برای این محصول وجود ندارد زیرا در دسته‌بندی پوشاک نیست.")
        super().save(*args, **kwargs)



# ============================================================================================================= #
# ==================================================== Brand ================================================== #
# ============================================================================================================= #



class Brand(models.Model):
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length = 50 , null=True)
    slug = models.SlugField(max_length = 50 , null=True)
    image = models.ImageField(upload_to = 'brand-photo' , null=True , blank=True)
    is_available = models.BooleanField(default = True)
    show_brand = models.BooleanField(default = False)

    def __str__(self):
        return '{}'.format(self.title)
    
    @property
    def images(self):
        return Image.objects.filter(
            object_id=self.id,
            content_type=ContentType.objects.get_for_model(self.__class__).id
        )
        
    def get_categories(self):
        return " , ".join([c.name for c in self.category.all()]) 

    def get_absolute_url(self):
        return reverse('app_store:product_detail', args=(self.id, ))
    
    def show_image(self):
        return format_html("<img src='{}' width=100 height=80 style='border-radius:10px;' >".format(self.image.url))
    show_image.short_description = 'Image'



# ============================================================================================================= #
# ==================================================== Banner ================================================= #
# ============================================================================================================= #



class Banner(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.title)
    
    @property
    def images(self):
        return Image.objects.filter(
            object_id=self.id,
            content_type=ContentType.objects.get_for_model(self.__class__).id
        )



# ============================================================================================================= #
# ==================================================== Image ================================================== #
# ============================================================================================================= #



class Image(models.Model):
    image = models.ImageField(upload_to='store/images/')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, related_name='app_store_images')
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return '{}'.format(self.content_type)
    
    def show_image(self):
        return format_html("<img src='{}' width=100 height=80 style='border-radius:10px;' >".format(self.image.url))
    show_image.short_description = 'Image'



# ============================================================================================================= #
# ==================================================== Description ============================================ #
# ============================================================================================================= #



class ProductDescription(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='descriptions')
    title = models.CharField(max_length=100 , blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return '{}'.format(self.title)