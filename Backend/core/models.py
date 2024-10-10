from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import re


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, email, full_name, password=None):
        if not phone_number:
            raise ValueError("The Phone Number field is required.")
        if not email:
            raise ValueError("The Email field is required.")
        
        phone_number = self.normalize_phone_number(phone_number)
        email = self.normalize_email(email)

        user = self.model(
            phone_number=phone_number,
            email=email,
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, email, full_name, password=None):
        user = self.create_user(phone_number, email, full_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    def normalize_phone_number(self, phone_number):
        phone_number = re.sub(r'\D', '', phone_number)

        if not re.match(r'^09\d{9}$', phone_number):
            raise ValueError("Invalid Persian phone number.")
        return phone_number


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.full_name
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser
    
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
