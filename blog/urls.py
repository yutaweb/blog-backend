from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    # https://qiita.com/kotayanagi/items/b97fe4a85b03cc6880ac
    path('', views.IndexView.as_view(), name='list'),
    path('create/', views.CreateArticleView.as_view(), name='create'),
    path('update/<slug:pk>/', views.UpdateArticleView.as_view(), name='update'),
    path('delete/<slug:pk>/', views.DeleteArticleView.as_view(), name='delete'),
    path('tags/<slug:slug>/', views.Tags.as_view(), name='tags'),
    path('<slug:pk>/', views.ArticleView.as_view(), name='detail'),
    path('<slug:pk>/like/', views.Like.as_view(), name='like'),
]
