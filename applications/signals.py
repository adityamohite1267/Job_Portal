from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Application

@receiver(post_save,sender=Application)
def send_status_email(sender,instance,**kwargs):

    if instance.status == "SHORTLISTED":

        send_mail(
            subject="Application Shortlisted ",
            message=f"Congratulations {instance.user.username}, your application for {instance.job.title} hs been shortlisted.",
            from_email="mohiteaditya7777@gmail.com",
            recipient_list=[instance.user.email],
        )
    elif instance.status == "REJECTED":
        send_mail(
            subject="Application Update",
            message=f"Hello {instance.user.username}, unfortunately your application for {instance.job.title} was not selected.Better Luck next time ",
            from_email="mohiteaditya7777@gmail.com",
            recipient_list=[instance.user.email],
        )

    elif instance.status == "HIRED":
        send_mail(subject="Congratulations! You're Selected ",
            message=f"Great news {instance.user.username}! You have been hired for {instance.job.title}.",
            from_email="mohiteaditya7777@gmail.com",
            recipient_list=[instance.user.email],

        )
    