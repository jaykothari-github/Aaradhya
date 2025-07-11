from django.shortcuts import render, redirect
from .models import *
from random import randrange,choices
import string
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
import qrcode
from PIL import Image
import os
from . import messages
from datetime import date

# Create your views here.

def index(request):
    try:
        email = request.session['email']
        student = Student.objects.get(email=email)
        return render(request, 'student/index.html', {'student':student})
    except:
        return render(request, 'student/index.html')

def register(request):
    try:
        email = request.session['email']
        student = Student.objects.get(email=email)
        return render(request, 'student/index.html', {'student':student})
    except:
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

        return render(request, 'student/register.html')


def otp(request):
    if request.method == "POST":
        sys_otp = request.POST['sys_otp']
        email = request.POST['email']
        user_otp = request.POST['user_otp']
        if sys_otp == user_otp:
            student  = Student.objects.get(email=email)
            
            ### QR experiment
            ################################################################
            Logo_link = os.path.join(settings.BASE_DIR,'media') + '/default/qr_logo.png'

            logo = Image.open(Logo_link)

            # taking base width
            basewidth = 120

            # adjust image size
            wpercent = (basewidth/float(logo.size[0]))
            hsize = int((float(logo.size[1])*float(wpercent)))
            logo = logo.resize((basewidth, hsize), 1)
            QRcode = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_H
            )

            url = f'https://aaradhyagroup.pythonanywhere.com/icard_profile?email={student.email}'
            # adding URL or text to QRcode
            QRcode.add_data(url)

            # generating QR code
            QRcode.make()

            # adding color to QR code
            QRimg = QRcode.make_image().convert('RGB')

            # set size of QR code
            pos = ((QRimg.size[0] - logo.size[0]) // 2,
                (QRimg.size[1] - logo.size[1]) // 2)
            QRimg.paste(logo, pos)

            user_name = str(student.first_name + "_" + student.last_name +"_" + email.split('@')[0])
            # save the QR code generated
            img_path = os.path.join(settings.BASE_DIR,'media') + '/profile_qr/' + user_name + '.png'
            QRimg.save(img_path)


            ###############################################
            ########### Simple QR #############
            ###############################################

            # ## QR code generate and save in folder
            # img = qrcode.make(f'https://markdjangopro1.pythonanywhere.com/icard_profile?email={student.email}')
            # img_path = os.path.join(settings.BASE_DIR,'media') + '/profile_qr/' + f"{student.first_name}_{student.last_name}" + '.png'
            # img.save(img_path)
            
            ###############################################

            ## url save in Database 
            student.profile_qr = 'profile_qr/' + user_name+ '.png'
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
    try:
        student = Student.objects.get(email=request.session['email'])
        return render(request, 'student/index.html', {'student':student})
    except:
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            if Student.objects.filter(email=email).exists():
                student = Student.objects.get(email=email)
                if student.password == password:
                    if student.verified:
                        if student.password_reset:
                            request.session['email'] = student.email
                            return render(request, 'student/index.html', {'student':student})
                        else:
                            return render(request, 'student/password_reset.html', { 'student':student ,'msg':'Please reset your password!! then complete your profile!!'})
                    else:
                        otp = randrange(1000,9999)
                        subject = 'OTP For Registration'
                        otp_msg = messages.otp_msg.format(fname=student.first_name , lname=student.last_name , otp=otp)
                        try:
                            send_mail(subject, otp_msg , settings.EMAIL_HOST_USER, [email])
                            msg = 'Email already register!! Please verify your OTP!!'
                            
                        except Exception as e:
                            msg = f'Error sending email: {e}'
                        return render(request, 'student/otp.html', {'email':email, 'otp':otp, 'msg':'Email not verified!! Please verify your email!!'})
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
        profile = Student.objects.get(email=email)
        try:
            student = Student.objects.get(email=request.session['email'])
            return render(request, 'student/icard_profile.html', {'student':student,'profile':profile})
        except:
            return render(request, 'student/icard_profile.html', {'profile':profile}) 
    except:
        return render(request, 'student/icard_profile.html', {'msg':'Invalid data!! Please try again!!'})
    
def password_reset(request):
    if request.method == "POST":
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        student = Student.objects.get(email=request.POST['email'])
        if password != cpassword:
            return render(request, 'student/password_reset.html', {'msg':'Password not matched!! Please try again!!', 'student':student})
        student.password = password
        student.password_reset = True
        student.save()
        
        return render(request, 'student/login.html', {'msg':'Password reset successfully!! Please login with new password!!'})
    
    return render(request, 'student/login.html')

def profile(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if request.method == "POST":
            
            if request.FILES.get('profile_image'):
                student.profile_image = request.FILES['profile_image']
                student.profile_image_verified = True
            if request.POST.get('password') and request.POST.get('cpassword'):
                if request.POST['password'] == request.POST['cpassword']:
                    student.password = request.POST['password']
                else:
                    return render(request, 'student/profile.html', {'student':student, 'msg':'Password and Confirm Password are not same!!'})
            student.aadhar = request.POST['aadhar']
            student.save()
            return render(request, 'student/profile.html', {'student':student, 'msg':'Profile updated successfully!!'})
        
        return render(request, 'student/profile.html', {'student':student})
    except:
        return render(request, 'student/login.html', {'msg':'Please login first!!'})
    

def icard(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        return render(request, 'student/icard.html', {'student':student})
    except:
        return render(request, 'student/login.html', {'msg':'Please login first!!'})

def enquiry(request):
    if request.method == "POST":
        name = request.POST['name']
        mobile = request.POST['mobile']
        
        Enquiry.objects.create(
            name = name,
            mobile = mobile
        )
        
    return redirect('index')

def student_event_list(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        events = Event.objects.filter(date__gte=date.today()).order_by('date')
        return render(request, 'student/student_event_list.html', {'student':student, 'events':events})
    except:
        return render(request, 'student/login.html', {'msg':'Please login first!!'})
    
def event_id_card(request, id):
    # try:
        student = Student.objects.get(email=request.session['email'])
        event = Event.objects.get(id=id)
        if event.title.strip() == 'Box Cricket':
            student_event_id = Cricket_Event.objects.filter(player=student, event=event).first()
            team_mates = Cricket_Event.objects.filter(event=event,  team=student_event_id.team).exclude(player=student)
            return render(request, 'student/cricket_idcard.html', {'student':student, 'team_mates': team_mates, 'event':event, 'student_event_id':student_event_id})
        return render(request, 'student/event_icard.html', {'student':student, 'event':event})
    # except:
    #     return render(request, 'student/login.html', {'msg':'Please login first!!'})