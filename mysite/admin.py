from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from mysite.models.account_models import User
from mysite.models.profile_models import Profile

from mysite.forms import UserCreationForm


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    fieldsets = (
        ("LOGIN INFO", {
            'fields': (
                'email',
                'password',
            )
        }),
        ("STATUS", {
            'fields': (
                'is_active',
                'is_admin',
            )
        })
    )

    list_display = ('email', 'is_active')
    list_filter = ()
    ordering = ()
    filter_horizontal = ()

    add_fieldsets = (
        (None, {
            'fields': ('email', 'password',),
        }),
    )

    add_form = UserCreationForm  # 管理画面から新規ユーザー登録


admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
