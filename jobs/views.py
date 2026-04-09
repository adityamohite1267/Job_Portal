from django.shortcuts import render,redirect,get_object_or_404
from .forms import JobForm,ApplicationForm
from .models import Job,Location
from applications.models import Application
from accounts.decorators import recruiter_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .utils import extract_resume_text,calculate_match_score

# Create your views here.

@login_required
@recruiter_required
def recruiter_dashboard(request):

    # recruiter jobs
    jobs = Job.objects.filter(recruiter=request.user)

    # applications for those jobs
    applications = Application.objects.filter(job__recruiter=request.user).select_related('job','applicant')
    
    #Analytics Counts
    total_jobs = jobs.count()
    total_applications = applications.count()

    shortlisted_count = applications.filter(status = "SHORTLISTED").count()
    rejected_count = applications.filter(status='REJECTED').count()
    hired_count = applications.filter(status = "HIRED").count()
    # ATS Filter
    filter_type = request.GET.get('filter')# Get the value of the "filter" parameter from the URL query string (?filter=...)
    if filter_type == "top":
        applications =applications.filter(match_score__gte = 60)  #gte means Greater Than Equel to  
    elif filter_type == "shortlisted":
        applications = applications.filter(
            status="SHORTLISTED")
    elif filter_type == "rejected":
        applications = applications.filter(
            status="REJECTED")
    
    context = {'jobs': jobs,'applications': applications,'current_filter':filter_type,
               'total_jobs':total_jobs,'total_applications':total_applications,
               'shortlisted_count':shortlisted_count,'rejected_count':rejected_count,'hired_count':hired_count}
    return render(request, 'jobs/recruiter_dashboard.html', context)

@login_required
@recruiter_required
def create_job_post(request):
   
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
            application.applicant.save()

            if not application.resume:
                profile = request.user.jobseekerprofile
                if profile.resume:
                    application.resume = profile.resume
                else:
                    messages.error(request, "Please Upload Resume.")
                    return redirect('jobs:job_detail', pk=job1.pk)

            

            #ATS match score logic add here
            try:
                resume_text = extract_resume_text(application.resume.file)
                score = calculate_match_score(job1.skills_required.all(),resume_text)
                application.match_score = score
                #auto shortlisted logic
                if score >=75:
                    application.status = 'SHORTLISTED'
                    application.save()
            except Exception:
                messages.error(request, "Error processing resume.")
                return redirect('jobs/job_detail.html',pk=job1.pk)

            application.save()

            
            messages.success(request, "Application Submitted Successfully!")
            return redirect('jobs:job_detail',pk=job1.pk)
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form,'job': job1})
   

@login_required
def my_applications(request):

    applications = Application.objects.filter(
        applicant=request.user
    ).select_related('job','job__recruiter')

    return render(request,"jobs/my_applications.html",{"applications": applications})

@login_required
def update_application_status(request,app_id,status):

    application = get_object_or_404(Application,id=app_id,job__recruiter=request.user)
    valid_status = [choice[0] for choice in Application.STATUS_CHOICES]

    if status not in valid_status:
        return redirect('jobs:recruiter_dashboard')

    application.status = status
    application.save()
    messages.success(request,f"Application marked as {status}")
    return redirect('jobs:recruiter_dashboard')