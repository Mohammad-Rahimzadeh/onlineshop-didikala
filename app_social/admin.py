from django.contrib import admin
from .models import IsUsefull , Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user' , 'product' , 'title' , 'rate' , 'is_suggest' , 'is_published' , 'like_count' , 'dislike_count']
    list_filter = ['is_published']


@admin.register(IsUsefull)
class IsUsfullAdmin(admin.ModelAdmin):
    list_display = ['comment' , 'is_useful']

