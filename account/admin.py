from django.contrib import admin
from .models import Account
from django.contrib.auth.models import Group, User


admin.site.unregister(Group)

admin.site.register(Account)
