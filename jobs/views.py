from django.shortcuts import render,redirect,get_object_or_404
from .forms import JobForm,ApplicationForm
from .models import Job,Location,Application
from accounts.decorators import recruiter_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.


@login_required
def recruiter_dashboard(request):

    # recruiter jobs
    jobs = Job.objects.filter(recruiter=request.user)

    # applications for those jobs
    applications = Application.objects.filter(job__recruiter=request.user).select_related('job','applicant')
    context = {'jobs': jobs,'applications': applications}
    return render(request, 'jobs/recruiter_dashboard.html', context)

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
    job_list = Job.objects.filter(is_active=True).order_by('-posted_at')

    paginator = Paginator(job_list, 3)
    page_number = request.GET.get('page')

    jobs = paginator.get_page(page_number)
    return render(request,'jobs/jobs_list.html',{'jobs':jobs})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)

    has_applied = False
    if request.user.is_authenticated and request.user.user_type == 'jobseeker':
        has_applied = Application.objects.filter(
            job=job,
            applicant=request.user
        ).exists()

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'has_applied': has_applied
    })

def toggle_job_status(request,job_id):
    job = get_object_or_404(Job,id=job_id,recruiter= request.user)
    job.is_active =  not job.is_active
    job.save()
    return redirect('jobs:recruiter_dashboard')

@login_required
def apply_job(request, pk):
    job1 = get_object_or_404(Job, pk=pk, is_active=True)

    if request.user.user_type != 'jobseeker':
        messages.error(request, "Only Job Seekers can apply.")
        return redirect('jobs:job_detail', pk=job1.pk)

    #show form
    if request.method == 'GET':
        form = ApplicationForm()
        return render(request, 'jobs/apply_job.html', {
            'form': form,
            'job': job1
        })

    #submit form
    if request.method == 'POST':

        # prevent duplicate applications
        if Application.objects.filter(job=job1, applicant=request.user).exists():
            messages.warning(request, "You have already applied.")
            return redirect('jobs:job_detail', pk=job1.pk)

        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)
            application.job = job1
            application.applicant = request.user

            if not application.resume:
                profile = request.user.jobseekerprofile
                if profile.resume:
                    application.resume = profile.resume
                else:
                    messages.error(request, "Please Upload Resume.")
                    return redirect('jobs:job_detail', pk=job1.pk)

            application.save()
            messages.success(request, "Application Submitted Successfully!")
            return redirect('jobs:job_detail', pk=job1.pk)

    return redirect('jobs:job_detail', pk=job1.pk)