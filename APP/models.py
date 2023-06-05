from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_salon = models.BooleanField(default=False)
    is_enduser = models.BooleanField(default=False)

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.otp


class OTP_temp(models.Model):
    otp = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(default=timezone.now)

@receiver(pre_save, sender=OTP_temp)
def delete_record_after_two_hours(sender, instance, **kwargs):
    current_time = timezone.now()
    if instance.created_at < current_time - timezone.timedelta(hours=2):
        instance.delete()

    
    
    