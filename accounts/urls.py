from django.urls import path
from .views import recruiter_login,recruiter_logout

urlpatterns = [
    path("recruiter/login",recruiter_login,name="recruiter_login"),
    path('recruiter/logout/',recruiter_logout,name="recruiter_logout")
]
