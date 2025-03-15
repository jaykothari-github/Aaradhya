from django.shortcuts import render
from .models import *
from random import randrange
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def index(request):
    return render(request, 'student/index.html')

def register(request):
    if request.method == "POST":

        Student.objects.create(
            first_name = request.POST['fname'],
            last_name = request.POST['lname'],
            birth_date = request.POST['bday'],
            email = request.POST['email'],
            mobile = request.POST['mobile'],
            parent_mobile = request.POST['pmobile'],
            address = request.POST['address'],
            password = request.POST['password'],
            aadhar = request.POST['aadhar']
            )
        email = request.POST['email']
        otp = randrange(1000,9999)
        subject = 'OTP for registration'
        message = f"""Your OTP is {otp}"""
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            # context['result'] = 'Email sent successfully'
        except Exception as e:
            msg = f'Error sending email: {e}'

        return render(request, 'student/otp.html', {'email':email, 'otp':otp})



        # aadhar_image = request.FILES['aadhar_image']
        # profile_qr = request.FILES['profile_qr']
        # profile_image = request.FILES['profile_image']
        return render(request, 'student/register.html')
    return render(request, 'student/register.html')


def otp(request):
    # if request.method == "POST":
    #     otp = request.POST['otp']
    #     email = request.POST['email']
    #     otp1 = request.POST['otp1']
    #     if otp == otp1:
    #         Student.objects.filter(email=email).update(verified=True)
    #         return render(request, 'student/login.html')
    #     else:
    #         return render(request, 'student/otp.html', {'email':email, 'otp':otp})
    # return render(request, 'student/otp.html')
    return render(request, 'student/otp.html')