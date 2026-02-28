from django.urls import path
from .views import create_job_post,recruiter_dashboard

app_name = "jobs"
urlpatterns = [
    path('create/', create_job_post, name='create_job_post'),
    path("dashboard/",recruiter_dashboard,name='recruiter_dashboard'),
]
