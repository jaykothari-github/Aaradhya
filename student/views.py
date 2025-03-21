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
    try:
        email = request.session['email']
        student = Student.objects.get(email=email)
        return render(request, 'student/index.html', {'student':student})
    except:
        return render(request, 'student/index.html')

def register(request):
    if request.method == "POST":

        email = request.POST['email']
        if Student.objects.filter(email=email).exists():
            student = Student.objects.get(email=email)
            if student.verified:
                return render(request, 'student/register.html', {'msg':'Email already exists!! Please try with another email!!'})
            else:
                otp = randrange(1000,9999)
                subject = 'OTP For Registration'
                otp_msg = messages.otp_msg.format(fname=student.first_name , lname=student.last_name , otp=otp)
                try:
                    send_mail(subject, otp_msg , settings.EMAIL_HOST_USER, [email])
                    msg = 'Email already register!! Please verify your OTP!!'
                    
                except Exception as e:
                    msg = f'Error sending email: {e}'
                return render(request, 'student/otp.html', {'email':email, 'otp':otp, 'msg':msg})
        else:
           
            otp = randrange(1000,9999)
            subject = 'OTP For Registration'
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


def otp(request):
    if request.method == "POST":
        sys_otp = request.POST['sys_otp']
        email = request.POST['email']
        user_otp = request.POST['user_otp']
        if sys_otp == user_otp:
            student  = Student.objects.get(email=email)
            
            ## QR code generate and save in folder
            img = qrcode.make(f'https://markdjangopro1.pythonanywhere.com/icard_profile?email={student.id}')
            img_path = os.path.join(settings.BASE_DIR,'media') + '/profile_qr/' + f"{student.first_name}_{student.last_name}" + '.png'
            img.save(img_path)
            
            ## url save in Database 
            student.profile_qr = 'profile_qr/' + f"{student.first_name}_{student.last_name}" + '.png'
            student.verified = True
            student.save()

            ## Email body msg
            msg = messages.welcome_msg.format(student=student)

            ## Email with attachment
            with open(img_path, 'rb') as f:
                msg = EmailMultiAlternatives("Welcome to Aaradhya group", msg, settings.EMAIL_HOST_USER, [student.email])
                msg.attach(f'{student.first_name}_{student.last_name}.png', f.read(), 'image/png')
                msg.send()

            return render(request, 'student/login.html',{'msg':'Email Verified!! Please Complete your profile by login!!'})
        else:
            return render(request, 'student/otp.html', {'email':email, 'otp':sys_otp,'msg':'Invalid OTP!! please Enter correct OTP!!'})
    return render(request, 'student/register.html')

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if Student.objects.filter(email=email).exists():
            student = Student.objects.get(email=email)
            if student.password == password:
                request.session['email'] = student.email
                return render(request, 'student/index.html', {'student':student})
            else:
                return render(request, 'student/login.html', {'msg':'Invalid Password!! Please try again!!'})
        else:
            return render(request, 'student/login.html', {'msg':'Email not found!! Please try again!!'})
    return render(request, 'student/login.html')

def logout(request):
    try:
        del request.session['email']
    except:
        pass
    return render(request, 'student/index.html')

def icard_profile(request):
    try:
        email = request.GET.get('email')
        student = Student.objects.get(email=email)
        return render(request, 'student/icard_profile.html', {'student':student})
    except:
        return render(request, 'student/icard_profile.html', {'msg':'Invalid data!! Please try again!!'})