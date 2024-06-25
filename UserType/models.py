from django.db import models
from django.contrib.auth.models import UserManager,AbstractBaseUser,AbstractUser




class CustomUser(AbstractUser):
    USER_TYPE = (
    
        (1, 'student'),
        (2, 'teacher'),
        (3, 'fakultet'),
        (4, 'uquv boshqarmasi'),
    )

    username = models.CharField(max_length=255, unique=True, verbose_name='Username')
    passwordinfo = models.CharField(max_length=255)
    user_type = models.IntegerField(choices=USER_TYPE, default=1, verbose_name='User Type')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archive = models.BooleanField(default=True)
    USERNAME_FIELD = 'username'
    objects = UserManager()

    REQUIRED_FIELDS = ['user_type']

    def __str__(self):
        return self.username


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
from django.contrib.auth import get_user_model


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    age = models.IntegerField()
    phone = models.CharField(max_length=255)
    studentid = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    age = models.IntegerField()
    phone = models.CharField(max_length=255)
    teacherid = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'


class Fakultet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    fakultetid = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Fakultet'
        verbose_name_plural = 'Fakultets'



    


class UquvBoshqarmasi(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'UquvBoshqarmasi'
        verbose_name_plural = 'UquvBoshqarmasis'

