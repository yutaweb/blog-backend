from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from mysite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login/',  views.Login.as_view()),
    path('logout/', LogoutView.as_view()),
    path('blog/', include('blog.urls')),
    path('signup/', views.signup),
]
