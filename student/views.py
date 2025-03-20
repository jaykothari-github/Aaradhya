from django.shortcuts import render
from .models import *
from random import randrange,choices
import string
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
import qrcode
import os
from . import messages

# Create your views here.

def index(request):
    return render(request, 'student/index.html')

def register(request):
    if request.method == "POST":

        if Student.objects.filter(email=request.POST['email']).exists():
            student = Student.objects.get(email=request.POST['email'])
            if student.is_verified:
                return render(request, 'student/register.html', {'msg':'Email already exists!! Please try with another email!!'})
            else:
                
                return render(request, 'student/register.html', {'msg':'Email already exists!! Please verify your email!!'})
        else:
           
            email = request.POST['email']
            otp = randrange(1000,9999)
            subject = 'OTP for registration'
            otp_msg = messages.otp_msg.format(fname=request.POST['fname'] , lname=request.POST['lname'], otp=otp)
            try:
                send_mail(subject, otp_msg , settings.EMAIL_HOST_USER, [email])
                msg = 'OTP sent to your email!!'
                Student.objects.create(
                    first_name = request.POST['fname'],
                    last_name = request.POST['lname'],
                    birth_date = request.POST['bday'],
                    email = request.POST['email'],
                    mobile = request.POST['mobile'],
                    parent_mobile = request.POST['pmobile'],
                    address = request.POST['address'],
                    password = ''.join(choices(string.ascii_letters + string.digits, k=8)),
                    aadhar = request.POST['aadhar']
                    )
            except Exception as e:
                msg = f'Error sending email: {e}'

            return render(request, 'student/otp.html', {'email':email, 'otp':otp, 'msg':msg})



        # aadhar_image = request.FILES['aadhar_image']
        # profile_qr = request.FILES['profile_qr']
        # profile_image = request.FILES['profile_image']
        return render(request, 'student/register.html')
    return render(request, 'student/register.html')


def otp(request):
    if request.method == "POST":
        sys_otp = request.POST['sys_otp']
        email = request.POST['email']
        user_otp = request.POST['user_otp']
        if sys_otp == user_otp:
            student  = Student.objects.get(email=email)
            
            ## QR code generate and save in folder
            img = qrcode.make(f'http://127.0.0.1:8000/qr/?id={student.id}')
            img_path = os.path.join(settings.BASE_DIR,'media') + '/profile_qr/' + f"{student.first_name}_{student.last_name}" + '.png'
            img.save(img_path)
            
            ## url save in Database 
            student.profile_qr = 'profile_qr/' + f"{student.first_name}_{student.last_name}" + '.png'
            student.verified = True
            student.save()

            msg = messages.welcome_msg.format(student=student)
            with open(img_path, 'rb') as f:
                msg = EmailMultiAlternatives("Welcome to Aaradhya group", msg, settings.EMAIL_HOST_USER, [student.email])
                msg.attach(f'{student.first_name}.png', f.read(), 'image/png')
                msg.send()

            return render(request, 'student/login.html',{'msg':'Email Verified!! Please Complete your profile by login!!'})
        else:
            return render(request, 'student/otp.html', {'email':email, 'otp':sys_otp,'msg':'Invalid OTP!! please Enter correct OTP!!'})
    # return render(request, 'student/otp.html',{'msg':'OTP verification'})