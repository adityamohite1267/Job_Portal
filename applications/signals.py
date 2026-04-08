from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Application

@receiver(pre_save,sender=Application)
def send_status_email(sender,instance,**kwargs):

    if not instance.pk:
        return
    previous = Application.objects.get(pk=instance.pk)
    if previous.status == instance.status:
        return
    
    if instance.status == "SHORTLISTED":
        send_mail(
            subject="Application Shortlisted ",
            message=f"Congratulations {instance.applicant.username}, your application for {instance.job.title} has been shortlisted.",
            from_email="mohiteaditya7777@gmail.com",
            recipient_list=[instance.applicant.email],)
    elif instance.status == "REJECTED":
        send_mail(
            subject="Application Update",
            message=f"Hello {instance.applicant.username}, unfortunately your application for {instance.job.title} was not selected.Better Luck next time ",
            from_email="mohiteaditya7777@gmail.com",
            recipient_list=[instance.applicant.email],)
    elif instance.status == "HIRED":
        send_mail(
            subject="Congratulations! You're Selected ",
            message=f"Great news {instance.applicant.username}! You have been hired for {instance.job.title}.",
            from_email="mohiteaditya7777@gmail.com",
            recipient_list=[instance.applicant.email],)
    