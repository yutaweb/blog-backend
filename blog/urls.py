from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('tags/<slug:slug>/', views.tags),
    path('<slug:pk>/', views.article),
]
