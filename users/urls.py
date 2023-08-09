from django.urls import path

from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('signup/', singup_view, name='signup'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('create_product/', create_product, name='create_product'),
    path('<str:slug>/edit_product/', edit_product, name='edit_product'),
    path('create_article/', create_article, name='create_article'),
    path('<str:slug>/edit_article/', edit_article, name='edit_article')
]