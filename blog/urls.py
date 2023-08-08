from django.urls import path
from .views import *

urlpatterns = [
    path('', BlogIndexView.as_view(), name='blog'),
    path('article/<str:slug>', ArticleDetailView.as_view(), name='article'),
    path('all_articles', AllArticlesView.as_view(), name='all_articles'),
    path('<str:slug>', ArticleByTag.as_view(), name='tag'),
    path('user_articles/<int:pk>', user_article_list, name='user_articles'),
]
