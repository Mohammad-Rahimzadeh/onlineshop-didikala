from django.contrib import admin
from .models import BlogCategory , Blog , BlogContent

# Create your modeladmin here.


class BlogContentInline(admin.TabularInline):
    model = BlogContent
    extra = 1


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['title' , 'is_available']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title' , 'get_categories' , 'author' , 'is_published' , 'created_date' , 'visit_count']
    inlines = [BlogContentInline]
