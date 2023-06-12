from django.urls import path
from django.contrib.auth.views import LogoutView
from mysite import views

app_name = 'mysite'
urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('mypage/', views.MypageView.as_view()),
    path('contact/', views.ContactView.as_view()),
    path('pay/', views.PayView.as_view()),
]
