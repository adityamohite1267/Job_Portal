from django.shortcuts import render,redirect
from .forms import JobForm
from accounts.decorators import recruiter_required
from django.contrib.auth.decorators import login_required

# Create your views here.
@recruiter_required
def create_job_post(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)  # Build object from form data but don't save yet
            job.recruiter = request.user.recruiterprofile  # Link job to recruiter's profile of logged-in user
            job.save()
            form.save_m2m()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request,"jobs/create_job.html",{'form':form})

@login_required
def recruiter_dashboard(request):
    return render(request,"jobs/recruiter_dashboard.html")

@login_required
def create_job(request):
    if request.user.user_type != 'recruiter':
        return redirect('/')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)  # Build object from form data but don't save yet
            job.recruiter = request.user  # Attach logged-in user as recruiter
            job.save()
            return redirect('job:recruiter_dashboard')
    else:
        form = JobForm()

    return render(request,'jobs/creat_job.html')