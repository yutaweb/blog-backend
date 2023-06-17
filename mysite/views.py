from django.shortcuts import render
from django.contrib.auth.views import LoginView
from blog.models import Article
from mysite.forms import UserCreationForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.core.mail import send_mail
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse_lazy
import os
import payjp
from .forms import (
    PasswordChangeForm, LoginForm,
    MyPasswordForm, MySetPasswordForm
)


class Index(View):

    def get(self, request):
        ranks = Article.objects.order_by('-count')[:2]  # 降順
        objs = Article.objects.all()[:3]
        context = {
            'title': 'toyama',
            'articles': objs,
            'ranks': ranks,
        }
        return render(request, 'mysite/index.html', context)


class Login(LoginView):
    form_class = LoginForm

    # バリデーション成功時に呼び出される
    def form_valid(self, form):
        messages.success(self.request, 'ログイン完了！')
        return super().form_valid(form)
    
    # バリデーション失敗時に呼び出される
    def form_invalid(self, form):
        messages.error(self.request, 'エラー！')
        return super().form_invalid(form)


class Signup(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('mysite:home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # self.objectにsave()されたuserオブジェクトが格納される
        valid = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, '登録完了！')
        return valid


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'mysite/password_change.html'
    success_url = reverse_lazy('mysite:password_change_done')


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'mysite/password_change_done.html'


class PasswordReset(PasswordResetView):
    form_class = MyPasswordForm
    subject_template_name = 'mail/subject.txt'
    email_template_name = 'mail/password_reset.html'
    template_name = 'mysite/password_reset.html'
    success_url = reverse_lazy('mysite:password_reset_done')

    # メーラーに表示されるメールタイトルを変更する


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'mysite/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    # 有効期限は3日（https://akiyoko.hatenablog.jp/entry/2021/12/01/080000）
    form_class = MySetPasswordForm
    success_url = reverse_lazy('mysite:password_reset_complete')
    template_name = 'mysite/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'mysite/password_reset_complete.html'


class MypageView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        return render(request, 'mysite/mypage.html', context)
    
    def post(self, request):
        context = {}
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)  # 紐づいているユーザーに対して保存する必要がある
            profile.user = request.user
            profile.save()
            messages.success(request, '更新完了しました！')
        return render(request, 'mysite/mypage.html', context)


class ContactView(View):
    context = {
        'grecaptcha_sitekey': os.environ['GRECAPTCHA_SITEKEY']
    }

    def get(self, request):
        return render(request, 'mysite/contact.html', self.context)

    def post(self, request):
        recaptcha_token = request.POST.get("g-recaptcha-response")
        res = grecaptcha_request(recaptcha_token)
        if not res:
            return messages.error(request, 'reCAPTCHA ERROR')

        subject = 'お問い合わせがありました'
        message = "お名前： {}\nメールアドレス： {}\n内容： {}"\
            .format(
                request.POST.get('name'),
                request.POST.get('email'),
                request.POST.get('content')
            )
        email_from = os.environ['DEFAULT_EMAIL_FROM']
        email_to = [os.environ['DEFAULT_EMAIL_FROM'], ]
        send_mail(subject, message, email_from, email_to)
        messages.success(request, 'お問い合わせ頂きありがとうございます。')
        return render(request, 'mysite/contact.html', self.context)


def grecaptcha_request(token):
    from urllib import request, parse
    import json
    import ssl
 
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
 
    url = "https://www.google.com/recaptcha/api/siteverify"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {
        'secret': os.environ['GRECAPTCHA_SECRETKEY'],
        'response': token,
    }
    data = parse.urlencode(data).encode()
    req = request.Request(
        url,
        method="POST",
        headers=headers,
        data=data,
    )
    f = request.urlopen(req, context=context)
    response = json.loads(f.read())
    f.close()
    return response['success']


class PayView(View):
    payjp.api_key = os.environ['PAYJP_SECRET_KEY']
    public_key = os.environ['PAYJP_PUBLIC_KEY']
    amount = 1000

    def get(self, request):
        context = {
            'amount': self.amount,
            'public_key': self.public_key,
        }
        return render(request, 'mysite/pay.html', context)

    def post(self, request):
        customer = payjp.Customer.create(
            email='example@pay.jp',
            card=request.POST.get('payjp-token')
        )
        charge = payjp.Charge.create(
            amount=self.amount,
            currency='jpy',
            customer=customer.id,
            description='支払いテスト'
        )
        context = {
            'amount': self.amount,
            'public_key': self.public_key,
            'charge': charge,
        }
        return render(request, 'mysite/pay.html', context)
