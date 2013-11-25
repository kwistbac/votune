from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from mJuke.models import Account


class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = "Other information"


class UserAdmin(UserAdmin):
    inlines = (AccountInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
