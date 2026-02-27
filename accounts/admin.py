from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,RecruiterProfile,JobSeekerProfile,Skill


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))

        fieldsets.append(
            ("Additional Info", {
                "fields": ("user_type","email", "phone", "profile_picture"),}))
        return fieldsets

    def get_add_fieldsets(self, request):
        fieldsets = list(super().get_add_fieldsets(request))
        fieldsets.append(
            ("Additional Info", {
                "fields": ("user_type", "phone", "profile_picture"),}))
        return fieldsets

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