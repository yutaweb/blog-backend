from django.urls import path, include
from mysite import views

urlpatterns = [
    path('', views.index),
    path('blog/', include('blog.urls')),
]
