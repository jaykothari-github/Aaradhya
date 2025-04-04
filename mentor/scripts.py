from student.models  import Student
from django.core.mail import send_mail, EmailMessage
from django.conf import settings



dp_pending = list(Student.objects.filter(profile_image_verified=False).values_list('email', flat=True))

subject = "Profile Image Verification Pending"
message = "Dear Student,\n\nOur AI has found that Your profile image verification is pending. Please upload your profile image for verification.\n\nThank you."
email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
email.bcc = dp_pending
email.send()