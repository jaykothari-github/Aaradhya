from django.db import models

# Create your models here.

class Student(models.Model):

    doc_choice = (
        ('Owner','Owner'),
        ('Sir','Sir'),
        ('Student','Student'),
    )


    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10)
    parent_mobile = models.CharField(max_length=10)
    role = models.CharField(max_length=10, choices=doc_choice, default='Student')
    address = models.TextField()
    password = models.CharField(max_length=30)
    verified = models.BooleanField(default=False)
    aadhar = models.CharField(max_length=12)
    aadhar_image = models.FileField(upload_to='aadhar/', blank=True, null=True)
    profile_qr = models.FileField(upload_to='profile_qr/',default='default/qr.png')
    profile_image = models.FileField(upload_to='profile/', default='default/profile.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name