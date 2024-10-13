from django.urls import path , include
from .views import blogView , singleBlogView

urlpatterns = [
    path('blog/', include('app_blog.api.urls')),
]