from django.contrib import admin
from .models import MyUser, MyItem


class MyUserAdmin(admin.ModelAdmin):
    model = MyUser


class MyItemAdmin(admin.ModelAdmin):
    model = MyItem


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(MyItem, MyItemAdmin)
