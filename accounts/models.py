from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):

    USER_TYPE_CHOICES = (('jobseeker', 'Job Seeker'),('recruiter', 'Recruiter'),)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20,choices=USER_TYPE_CHOICES,)
    phone = models.CharField(max_length=15,blank=True,null=True)
    profile_picture = models.ImageField(upload_to='profiles/',blank=True,null=True)
    REQUIRED_FIELDS = ['email', 'user_type']

    def __str__(self):
        return f"{self.username} ({self.user_type})"
    
    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

# create seprate profiles models to avoid messiness in customuser 
class RecruiterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_website = models.URLField(blank=True,null=True)
    company_description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.company_name
    
#skill model will help in jobseekerprofile  
class Skill(models.Model):
    name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/',blank=True,null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    experience = models.IntegerField(default=0)
    education = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
    