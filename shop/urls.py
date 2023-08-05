from django.urls import path
from .views import *

urlpatterns = [
    path('', CatalogIndexView.as_view(), name='catalog'),
    path('<slug:slug>/', BookByCategory.as_view(), name='category'),
    path('book/<str:slug>/', BookDetailView.as_view(), name='book'),
    path('user_books/<int:pk>', user_book_list,name='user_books'),
    path('search/', search, name='search'),
    
    # Для работы с изображениями
    path('delete_image/<str:slug>/<int:pk>', delete_image, name='delete_image'),
    path('set_main_image/<str:slug>/<int:pk>', set_main_image, name='set_main_image'),
]
