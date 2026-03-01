from django.urls import path
from .views import create_job_post,recruiter_dashboard,job_list,job_detail,toggle_job_status

app_name = "jobs"
urlpatterns = [
    path('create/', create_job_post, name='create_job_post'),
    path("dashboard/",recruiter_dashboard,name='recruiter_dashboard'),
    path('',job_list,name='joblist'),
    path("job/<int:pk>",job_detail,name="job_detail"),
    path('job/<int:job_id>/toggle/',toggle_job_status, name='toggle_job_status'),
]
