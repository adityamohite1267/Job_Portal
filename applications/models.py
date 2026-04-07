from django.db import models
from django.conf import settings
# Create your models here.
class Application(models.Model):
    STATUS_CHOICES = (('APPLIED','Applied'),('UNDER_REVIEW','Under Review'),('SHORTLISTED','Shortlisted'),('REJECTED','Rejected'),('HIRED','Hired'),) #('Database_value','Display Value')
    job = models.ForeignKey('jobs.Job',on_delete=models.CASCADE,related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='applications')
    resume =models.FileField(upload_to='application_resumes/')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='APPLIED')
    match_score = models.IntegerField(null=True,blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'jobs_application'
        unique_together = ('job','applicant')  #One user can apply only once per job
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant.email} applied to {self.job.title}"