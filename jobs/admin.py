from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title","company_name","job_type","salary",'is_active','posted_at')
    search_fields = ("title","company_name",'location__city')
    list_filter = ("job_type",'is_active','posted_at')
    filter_horizontal = ("skills_required",)
    ordering = ("-posted_at",)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", "state", "country")
    search_fields = ("city", "state")
    list_filter = ("state", "country")

