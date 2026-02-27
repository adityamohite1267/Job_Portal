from django.db import models
from django.conf import settings
# Create your models here.
class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100,default='India')

    def __str__(self):
        return f"{self.city},{self.state}"

class Job(models.Model):
    JOB_TYPE_CHOICES = (('FULL_TIME','Full_Time'),('PART_TIME','Part_Time'),
                        ('INTERNSHIP','Internship'))
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
                                  limit_choices_to={'user_type':'RECRUITER'})
    
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)   # after next create Location model
    description = models.TextField()
    skills_required = models.ManyToManyField('accounts.Skill')  # Skill model in other apps that's why I use the string reference with the app label / 'accounts.Skill' like this
    job_type = models.CharField(max_length=25, choices=JOB_TYPE_CHOICES)
    salary = models.PositiveIntegerField()
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} - {self.company_name}"
    