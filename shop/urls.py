from django.urls import path
from .views import *

urlpatterns = [
    path('', CatalogIndexView.as_view(), name='catalog'),
    path('<slug:slug>/', BookByCategory.as_view(), name='category'),
    path('book/<str:slug>/', BookDetailView.as_view(), name='book'),
]
