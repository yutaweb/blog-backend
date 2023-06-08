from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='list'),
    path('tags/<slug:slug>/', views.tags),
    path('<slug:pk>/', views.article),
    path('<slug:pk>/like/', views.like),
]
