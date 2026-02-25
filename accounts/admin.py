from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))

        fieldsets.append(
            ("Additional Info", {
                "fields": ("user_type", "phone", "profile_picture"),
            })
        )

        return fieldsets

    def get_add_fieldsets(self, request):
        fieldsets = list(super().get_add_fieldsets(request))

        fieldsets.append(
            ("Additional Info", {
                "fields": ("user_type", "phone", "profile_picture"),
            })
        )

        return fieldsets