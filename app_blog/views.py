from django.shortcuts import render
from .models import Blog , BlogCategory

# Create your views here.


def blogView(request):
    blog = Blog.objects.filter(is_published='published')
    blog_category = BlogCategory.objects.all()
    
    context = {
        'blog' : blog , 
        'blog_category' : blog_category
    }
    
    return render(request , 'app_blog/blog.html' , context)



def singleBlogView(request , slug):
    single_blog = Blog.objects.get(slug=slug)
    
    context = {
        'single_blog':single_blog ,
    }
    
    return render(request , 'app_blog/single-blog.html' , context)