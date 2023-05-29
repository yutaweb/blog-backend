from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)
from django.contrib.auth import get_user_model
from mysite.models.profile_models import Profile

import re


class UserCreationForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = get_user_model()
        fields = ('email',)
    
    def clean_password(self):  # is_validされたデータが入る
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'username',
            'zipcode',
            'prefecture',
            'city',
            'address',
            'image',
        )
        # exclude = ('user',) でも可能


class MyPasswordForm(PasswordResetForm):
    """
        用途：パスワード紛失時のフォーム
        参考：https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/forms/
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not get_user_model()._default_manager.filter(
            email__iexact=email, is_active=True
        ).exists():
            raise forms.ValidationError('有効なメールアドレスを入力して下さい。', 'invalid_mail_address')
        return email


class MySetPasswordForm(SetPasswordForm):
    """
        用途：パスワード再設定用フォーム
        参考：https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/forms/
    """
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if len(password1) < 8:
            raise forms.ValidationError('パスワードは最低8文字以上必要です。', 'short_password')
        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('確認用パスワードを一致させてください。', 'password_mismatch')
        if password2.lower() in self.user.email.lower():
            raise forms.ValidationError('パスワードがメールアドレスと似ています。', 'password_mismatch')
        regex = re.compile('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[?|@#$%]).{8,16})')
        if regex.search(password1) is None:
            raise forms.ValidationError('パスワード条件に準拠していません。', code='password_mismatch')
        return password2
