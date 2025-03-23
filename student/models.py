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
    password_reset = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    aadhar = models.CharField(max_length=12)
    aadhar_image = models.FileField(upload_to='aadhar/', blank=True, null=True)
    aadhar_verified = models.BooleanField(default=False)
    profile_qr = models.FileField(upload_to='profile_qr/',default='default/qr.png')
    profile_image = models.FileField(upload_to='profile/', default='default/profile.jpg')
    profile_image_verified = models.BooleanField(default=False)
    fees_amount = models.IntegerField(default=0)
    fees_paid = models.IntegerField(default=0)
    fees_status = models.BooleanField(default=False)
    batch_name = models.CharField(max_length=30, blank=True, null=True, default='General')
    batch_start_date = models.DateField(blank=True, null=True)
    batch_end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name