from django.shortcuts import render,redirect
from django.contrib.auth import login
from .forms import LoginForm,SignUpForm
from django.contrib import messages
# Create your views here.

def login_view(request):
    next_url = request.POST.get('next') or request.GET.get('next')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request,user)
            
            messages.success(request,"Login Successfull!")

            # IMPORTANT: redirect to next if exists
            if next_url:
                return redirect(next_url)
            
            if user.user_type == 'recruiter':
                return redirect('jobs:recruiter_dashboard')
            elif user.user_type == 'jobseeker':
                return redirect('jobs:joblist')
    else:
        form = LoginForm()
    return render(request,"accounts/login.html",{"form": form,'next':next_url})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = SignUpForm()
    return render(request,'accounts/signup.html',{'form':form})