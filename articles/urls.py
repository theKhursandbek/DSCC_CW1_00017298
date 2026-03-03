from django.urls import path
from .views import (
    ArticleListView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleCreateView,
    like_article,
)

urlpatterns = [
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('<int:pk>/like/', like_article, name='article_like'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('new/', ArticleCreateView.as_view(), name='article_new'),
    path('', ArticleListView.as_view(), name='article_list'),
]
