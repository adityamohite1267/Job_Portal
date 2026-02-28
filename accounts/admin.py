from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,RecruiterProfile,JobSeekerProfile,Skill


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Fields shown when EDITING a user
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Additional Info", {"fields": ("user_type", "phone", "profile_picture")}),)

    # Fields shown when ADDING a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "user_type", "phone", "profile_picture"),}),)

    list_display = ("username", "email", "user_type", "is_staff")

@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ("user","company_name","created_at")
    search_fields = ("company_name","user__username","user__email")
    list_filter = ("created_at",)# here use comma because it is a tuple not string

@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "experience", "education", "created_at")
    search_fields = ("user__username", "user__email", "education")
    list_filter = ("experience", "created_at")
    filter_horizontal = ("skills",) # it is ManyToMany UI improvement

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)