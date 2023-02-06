from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, name, password, **other_fields):
        if not email:
            raise ValueError(gettext_lazy('You must provide an email address'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff')
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assgined to is_superuser')
        
        return self.create_user(email, name, password, **other_fields)

class User(AbstractBaseUser, PermissionsMixin):
    CONTRACT_CHOICES = [
        ('Employee', 'Employee'),
        ('Subcontractor', 'Subcontractor')
    ]

    email = models.EmailField(gettext_lazy('Email address'), unique=True)
    name = models.CharField(max_length=50, blank=False)
    country = models.CharField(max_length=50, blank=False)
    contract_type = models.CharField(max_length=50, choices=CONTRACT_CHOICES, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'country', 'contract_type']

    def __str__(self):
        return f'{self.email}'