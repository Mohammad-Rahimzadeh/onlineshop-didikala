from django.urls import path
from app_account import views
from app_social.views import deleteCommentView

urlpatterns = [
    path('login/', views.loginView , name = 'login'),
    path('signup/', views.signupView , name = 'signup'),
    path('welcome/', views.welcomeView , name = 'welcome'),
    path('logout/', views.logoutView , name = 'logout'),
    path('change-password/', views.changePasswordView , name = 'change_password'),

    path('profile/', views.profileView , name = 'profile'),
    path('edit-profile/', views.editProfileView , name = 'edit-profile'),
    path('privacy/', views.privacyView , name = 'privacy'),
    path('personal-info/', views.personalInfoView , name = 'personal-info'),

    path('favorites/', views.profileFavoritesView , name = 'favorites'),
    path('favorite/add/<int:product_id>/', views.addToFavoriteView, name='add_to_favorite'),
    path('favorite/remove/<int:item_id>/', views.removeFromFavoriteView, name='remove_from_favorite'),

    path('addresses/', views.profileAddressView , name = 'addresses'),
    path('address/add/', views.addAddressView , name='add_address'),
    path('address/<int:address_id>/edit/', views.editAddressView, name='edit_address'),
    path('address/<int:address_id>/delete/', views.removeAddressView , name='delete_address'),
    
    path('comments/', views.profileCommentsView , name = 'comments'),
    path('comments/<int:comment_id>/delete/', deleteCommentView , name='delete_comment'),
]