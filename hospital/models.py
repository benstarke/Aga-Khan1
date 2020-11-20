from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model
from django.utils import timezone


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, name, password, **extra_fields):
        values = [email, name]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, password, **extra_fields)

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, name, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    #username = models.CharField(max_length=150)
    #phone = models.CharField(max_length=150)
    first_name = models.CharField(max_length=50)
    Gender = models.CharField(max_length=500,default="Male", blank=False)
    birth_date = models.DateField(null=True,default="2000-1-1", blank=False)
    location = models.CharField(max_length=30,default="Nairobi" ,blank=True)
    #birth_date = models.DateField(blank=True, null=True)
    picture = models.ImageField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split()[0]

class Patient(models.Model):
    name = models.CharField(max_length=255)
    gender  = models.CharField(max_length=255)
    email = models.EmailField()
    #doctor_id = models.IntegerField()

class Appointment(models.Model):
    #Patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Fname = models.CharField(max_length=255)
    Lname = models.CharField(max_length=255)
    id_number = models.IntegerField()
    Gender = models.CharField(max_length=255)
    Typeofdisease = models.CharField(max_length=255)
    message = models.CharField(max_length=255)

    def __str__(self):
        return self.Fname



class Doctor(models.Model):
    doctor_name = models.CharField(max_length=255)
    doctor_email = models.EmailField()
    #patient_id = models.IntegerField()
    doctor_field = models.CharField(max_length=255)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

class Hospital(models.Model):
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    #patient_id = models.IntegerField()
    location = models.CharField(max_length=255)
    email = models.EmailField()
    #doctor_id = models.IntegerField()

class Services(models.Model):
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    #Patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=255)
    #patient_id = models.IntegerField()
    description = models.TextField(max_length=255)
    treatment = models.TextField()
    drugs = models.CharField(max_length=255)