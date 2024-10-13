from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from .models import Category , Product , Color , Brand , Banner , Image , Size , ProductDescription


# ============================================== Actions ===================================================== #

@admin.action(description="محصولات انتخاب شده را به حالت انتشار تغییر وضعیت بده")
def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)
    
@admin.action(description="محصولات انتخاب شده را به حالت پیش نویس تغییر وضعیت بده")
def make_draft(modeladmin, request, queryset):
    queryset.update(is_published=False)
    
@admin.action(description="تغییر وضعیت پیشنهادی برای محصولات انتخاب شده")
def is_suggested(modeladmin, request, queryset):
    if is_suggested is True:
        queryset.update(is_suggested=False)
    else:
        queryset.update(is_suggested=True) 

# ============================================== Inlines ===================================================== #


class ImageInline(GenericStackedInline):
    model = Image
    extra = 1


class ProductDescriptionInline(admin.TabularInline):
    model = ProductDescription
    extra = 20
    


# ================================================================================================================== #
# ============================================== CategoryAdmin ===================================================== #


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name' , 'slug' , 'parent' , 'is_available']
    list_filter = ['is_available']
    prepopulated_fields = {'slug' : ('name' ,)}
    ordering = ['parent__id']

# ============================================== ProductProductAdmin ===================================================== #


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name_fa' , 'model' , 'brand' , 'get_categories' , 'price' , 'count' , 'rate' , 'is_published' , 'is_suggested' , 'visit_count']
    inlines = [ImageInline , ProductDescriptionInline]
    actions = [make_published , make_draft , is_suggested]


# ============================================== ColorAdmin ===================================================== #


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['get_products' , 'color_name']
    
    
# ============================================== ColorAdmin ===================================================== #


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['get_products' , 'size']
    

# ============================================== BrandAdmin ===================================================== #


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['title' , 'show_image' , 'get_categories' , 'is_available' , 'show_brand']
    prepopulated_fields = {'slug' : ('title' ,)}
    list_editable = ['show_brand']


# ============================================== ImageAdmin ===================================================== #


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['content_type' , 'show_image']
    list_filter = ['content_type']
        
            
# ============================================== BannerAdmin ===================================================== #


@admin.register(Banner)    
class BannerAdmin(admin.ModelAdmin):
    inlines = [ImageInline]