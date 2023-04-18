from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('tags/<slug:slug>/', views.tags),
    path('<slug:pk>/', views.article),
]
