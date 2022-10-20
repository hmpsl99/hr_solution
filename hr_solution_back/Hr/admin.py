from django.contrib import admin

from .models import Profile, Salary, User


class ProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields]


class SalaryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Salary._meta.fields]


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "link", "role"]

    readonly_fields = ["link"]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(User, UserAdmin)
