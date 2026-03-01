from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .forms import JobForm
from .models import Job,Location
from accounts.decorators import recruiter_required
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def recruiter_dashboard(request):
    jobs =Job.objects.filter(recruiter=request.user)
    return render(request,"jobs/recruiter_dashboard.html",{'jobs':jobs})

@login_required
def create_job_post(request):
    if request.user.user_type != 'recruiter':
        return redirect('/')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)  # Build object from form data but don't save yet

            city = form.cleaned_data['city'].strip().title()
            state = form.cleaned_data['state'].strip().title()

            #get or create location
            location,created= Location.objects.get_or_create(city = city , state = state)
            job.location = location
            job.recruiter = request.user  # Attach logged-in user as recruiter
            job.save() #saves the job, gives it an ID
            form.save_m2m()# Save many-to-many relationships (like in our skills) after job has an ID
            return redirect('jobs:recruiter_dashboard')
    else:
        form = JobForm()

    return render(request,'jobs/create_job.html',{"form":form})

def job_list(request):
    jobs = Job.objects.all().order_by('-posted_at')
    return render(request,'jobs/jobs_list.html',{'jobs':jobs})

def job_detail(request,pk):
    job = get_object_or_404(Job,pk=pk)
    return render(request,"jobs/job_detail.html",{"job":job})

def toggle_job_status(request,job_id):
    job = get_object_or_404(Job,id=job_id,recruiter= request.user)
    job.is_active =  not job.is_active
    job.save()
    return redirect('jobs:recruiter_dashboard')