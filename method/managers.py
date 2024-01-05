from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    
    def create_user(self, phone_number, password = None, verification_method = 'sms',**extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number field is required")
        
        user = self.model(phone_number = phone_number, verification_method = verification_method,**extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, phone_number, password = None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(phone_number,password, verification_method='sms',**extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user