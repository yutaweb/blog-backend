from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='list'),
    path('tags/<slug:slug>/', views.tags, name='tags'),
    path('<slug:pk>/', views.ArticleView.as_view(), name='detail'),
    path('<slug:pk>/like/', views.like),
]
