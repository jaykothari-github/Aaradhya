from django.db import models

# Create your models here.

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10)
    parent_mobile = models.CharField(max_length=10)
    address = models.TextField()
    password = models.CharField(max_length=30)
    verified = models.BooleanField(default=False)
    aadhar = models.CharField(max_length=12)
    aadhar_image = models.FileField(upload_to='aadhar/')
    profile_image = models.FileField(upload_to='profile/', default='profile/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name