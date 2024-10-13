from django.urls import path
from app_store import views
from app_social.views import addCommentView , vote_comment


urlpatterns = [
    path('', views.homeView , name = 'home'),
    path('all-products', views.productListView , name = 'all_products'),
    
    path('all-products/most-visited-products', views.productListView , name = 'most_visited_products'),
    path("all-products/search/", views.productListView, name="search_results"),
    path('products/<int:id>/' , views.productDetailView, name = 'product_detail'),
    
    path('not-found/', views.notFoundView , name = 'not-found'),
    
    path('products/filter', views.productFilterView, name='product_filter') ,
    
    path('brands/<slug:slug>', views.brandsView , name = 'brands'),
    
    path('categories/<slug:slug>', views.categoryView , name = 'categories'),
    
    path('products/<int:id>/add-comment' , addCommentView, name = 'add_comment'),
    path('vote-comment/<int:product_id>/<int:comment_id>/', vote_comment, name='vote_comment'),
    
]