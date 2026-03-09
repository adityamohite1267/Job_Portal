from django.shortcuts import render,redirect
from django.contrib.auth import login, logout
from .forms import LoginForm
from django.contrib import messages
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request,user)
            
            messages.success(request,"Login Successfull!")

            if user.user_type == 'recruiter':
                return redirect('jobs:recruiter_dashboard')
            elif user.user_type == 'jobseeker':
                return redirect('jobs:joblist')
    else:
        form = LoginForm()
    return render(request,"accounts/login.html",{"form": form})
