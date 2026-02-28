from django.shortcuts import render,redirect
from django.contrib.auth import login, logout
from .forms import RecruiterLoginForm
# Create your views here.

def recruiter_login(request):
    if request.method == 'POST':
        form = RecruiterLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request,user)
            return redirect('jobs:recruiter_dashboard')
    else:
        form = RecruiterLoginForm()
    return render(request,"accounts/recruiter_login.html",{"form": form})
def recruiter_logout(request):
    logout(request)
    return redirect("recruiter_login")