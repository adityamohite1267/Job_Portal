from django.contrib import admin
from .models import Application
# Register your models here.
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job','applicant','status','applied_at')
    list_filter = ('status',)
    search_fields = ('job__title','applicant__email') 