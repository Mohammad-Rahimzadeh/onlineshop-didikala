from django.urls import path, include
from app_blog.api import views

urlpatterns = [
    path('list/', views.blogListView, name='blog-list'),  
    path('<int:id>/', views.blogDetailView, name='blog-detail'),  
    path('delete/', views.blogDeleteView, name='blog-delete'),
    path('create/', views.blogCreateView.as_view(), name='blog-create'),
    path('<int:pk>/update/', views.blogUpdateView.as_view(), name='blog-update'),

    path('content/create/', views.blogContentCreateView.as_view(), name='blog-content-create'),

    path('category/list/', views.blogcategoryListView, name='blog-category-list'),  
    path('category/create/', views.BlogCategoryCreateSerializer.as_view(), name='blog-category-create'),
]