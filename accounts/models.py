from django.contrib.auth.models import AbstractUser
from .usermanager import CustomUserManager
from django.conf import settings
from django.db import models
from django.utils import timezone
import datetime
# Create your models here.
class CustomUser(AbstractUser):
    username = None
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    
class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField()
    create_at = models.DateTimeField(auto_now_add=True)
    
    
    def is_expire(self):
        return  timezone.now() > self.create_at + datetime.timedelta(minutes=5)