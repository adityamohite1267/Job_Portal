from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path("login/",login_view,name="login"),
    path('recruiter/logout/',recruiter_logout,name="recruiter_logout")
]
