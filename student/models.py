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
    aadhar_verified = models.BooleanField(default=False)
    aadhar_verified_by = models.CharField(max_length=30,blank=True,null=True)
    profile_qr = models.FileField(upload_to='profile_qr/',default='default/qr.png')
    profile_image = models.FileField(upload_to='profile/', default='default/profile.jpg')
    profile_image_verified = models.BooleanField(default=False)
    fees_amount = models.IntegerField(default=0)
    fees_paid = models.IntegerField(default=0)
    fees_status = models.BooleanField(default=False)
    fees_marker = models.CharField(max_length=30,blank=True,null=True)
    batch_name = models.CharField(max_length=30, blank=True, null=True, default='General')
    batch_start_date = models.DateField(blank=True, null=True)
    batch_end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    block  = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + " " + self.last_name
    

class Enquiry(models.Model):
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
class StudentFeedback(models.Model):
    # student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"Feedback from {self.student.first_name} {self.student.last_name}"

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    day = models.CharField(max_length=10)
    time = models.TimeField()
    location = models.CharField(max_length=100)
    location_link = models.URLField(blank=True, null=True)
    charges = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    dress_code = models.CharField(max_length=50, blank=True, null=True)
    event_image = models.FileField(upload_to='event_images/', null=True, blank=True)
    event_image_alt_text = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title
    
class Cricket_Team(models.Model):

    name = models.CharField(max_length=50)
    captain = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='team_captain')
    dress_code = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - Captain: {self.captain.first_name} {self.captain.last_name}"
     
class Cricket_Event(models.Model):
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.ForeignKey(Cricket_Team, on_delete=models.CASCADE, related_name='team')
    player = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='player')
    event_fees = models.IntegerField(default=0)
    fees_status = models.BooleanField(default=False) 


    def __str__(self):
        return f"{self.event.title} - ({self.player.first_name} {self.player.last_name})" 
    
