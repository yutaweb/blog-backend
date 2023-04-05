from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from blog.models import Article
from mysite.forms import UserCreationForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.mail import send_mail
import os


def index(request):
    ranks = Article.objects.order_by('-count')[:2]  # 降順
    objs = Article.objects.all()[:3]
    context = {
        'title': 'toyama',
        'articles': objs,
        'ranks': ranks,
    } 
    return render(request, 'mysite/index.html', context)


class Login(LoginView):
    template_name = 'mysite/auth.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'ログイン完了！') 
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'エラー！')
        return super().form_invalid(form)


def signup(request):
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # 新規登録後にそのままログインさせる
            login(request, user)

            messages.success(request, '登録完了！')
            return redirect('/')
    return render(request, 'mysite/auth.html', context)

@login_required
def mypage(request):
    context = {}
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)  # 紐づいているユーザーに対して保存する必要がある
            profile.user = request.user
            profile.save()
            messages.success(request, '更新完了しました！')
    return render(request, 'mysite/mypage.html', context)


def contact(request):
    context = {}
    if request.method == "POST":
        subject = 'お問い合わせがありました'
        message = "お名前： {}\nメールアドレス： {}\n内容： {}"\
            .format(
                request.POST.get('name'),
                request.POST.get('email'),
                request.POST.get('content')
            )
        email_from = os.environ['DEFAULT_EMAIL_FROM']
        email_to = [os.environ['DEFAULT_EMAIL_FROM'],]
        send_mail(subject, message, email_from, email_to)
        messages.success(request, 'お問い合わせ頂きありがとうございます。')

    return render(request, 'mysite/contact.html', context)
