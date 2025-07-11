from django.shortcuts import render
from student.models import *
from django.db.models import Q
from django.shortcuts import redirect
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from student.messages import *
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            student = Student.objects.get(email=email)
            if student.password == password:
                if student.role == 'Student':
                    return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
                request.session['email'] = email
                return redirect('mentor-index')
            else:
                return render(request, 'login.html', {'msg': 'Invalid credentials'})
        except:
            return render(request, 'login.html', {'msg': 'Invalid credentials'})
    return render(request, 'login.html')

def index(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        students = Student.objects.all()
        students_count = students.filter(role='Student').count() 
        fees_pending = students.filter(fees_status=False).count()
        pending_verification = students.filter( Q(profile_image_verified=False) | Q(aadhar_verified=False)).exclude(verified=False).order_by('created_at')[:8]
        all_verified = students.filter(fees_status=True, verified=True, password_reset=True, profile_image_verified=True, aadhar_verified=True ).count() 
        unverified_list = students.filter(Q(verified=False) | Q(password_reset=False)).order_by('first_name','created_at')
        aadhar_unverified = students.filter(aadhar_verified=False).count()
        profile_unverified = students.filter(profile_image_verified=False).count()
        return render(request, 'index.html', {'students_count': students_count, 
                                              'unverified_list': unverified_list,
                                              'pending_verification': pending_verification,
                                              'student': student, 
                                              'fees_pending': fees_pending, 
                                              'all_verified': all_verified, 
                                              'aadhar_unverified': aadhar_unverified, 
                                              'profile_unverified': profile_unverified})
    except:
        return render(request, 'login.html')


def delete_profile(request, id):
    try:
        sir = student = Student.objects.get(email=request.session['email'])
        if sir.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        student = Student.objects.get(id=id)
        student.delete()
        return redirect('mentor-index')
    except:
        return redirect('mentor-index')
    
def students_list(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            students = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(mobile__icontains=search) | Q(aadhar__icontains=search), role='Student').order_by('id')
            return render(request, 'students_list.html', {'students': students, 'student': student, 'msg': f'Search results for "{search}"' })
        
        students = Student.objects.filter(role='Student')
        return render(request, 'students_list.html', {'students': students, 'student': student})
    
    except:
        return render(request, 'login.html')
    
def fees_paid_list(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            students = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(mobile__icontains=search) | Q(aadhar__icontains=search), fees_status=True).order_by('id')
            return render(request, 'fees_paid_list.html', {'students': students, 'student': student, 'msg': f'Search results for "{search}"' })
        
        students = Student.objects.filter(fees_status=True)
        return render(request, 'fees_paid_list.html', {'students': students, 'student': student})
    
    except:
        return render(request, 'login.html')
    
def fees_unpaid_list(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            students = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(mobile__icontains=search) | Q(aadhar__icontains=search), fees_status=False).order_by('id')
            return render(request, 'fees_unpaid_list.html', {'students': students, 'student': student, 'msg': f'Search results for "{search}"' })
        
        students = Student.objects.filter(fees_status=False)
        return render(request, 'fees_unpaid_list.html', {'students': students, 'student': student})
    
    except:
        return render(request, 'login.html')
    
def all_verified(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            students = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(mobile__icontains=search) | Q(aadhar__icontains=search), fees_status=True, profile_image_verified=True, aadhar_verified=True).order_by('id')
            return render(request, 'all_verified.html', {'students': students, 'student': student, 'msg': f'Search results for "{search}"' })
        
        students = Student.objects.filter(fees_status=True, profile_image_verified=True, aadhar_verified=True)
        return render(request, 'all_verified.html', {'students': students, 'student': student})
    
    except:
        return render(request, 'login.html')


def sir_list(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            students = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(mobile__icontains=search) | Q(aadhar__icontains=search), role='Sir').order_by('id')
            return render(request, 'sir_list.html', {'students': students, 'student': student, 'msg': f'Search results for "{search}"' })
        
        students = Student.objects.filter(role='Sir')
        return render(request, 'sir_list.html', {'students': students, 'student': student})
    
    except:
        return render(request, 'login.html')


def profile_image_verified_list(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            students = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(mobile__icontains=search) | Q(aadhar__icontains=search), profile_image_verified=True).order_by('id')
            return render(request, 'profile_image_verified_list.html', {'students': students, 'student': student, 'msg': f'Search results for "{search}"' })
        
        students = Student.objects.filter(profile_image_verified=True)
        return render(request, 'profile_image_verified_list.html', {'students': students, 'student': student})
    
    except:
        return render(request, 'login.html')
    

def profile_image_unverified_list(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            students = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(mobile__icontains=search) | Q(aadhar__icontains=search), profile_image_verified=False).order_by('id')
            return render(request, 'profile_image_unverified_list.html', {'students': students, 'student': student, 'msg': f'Search results for "{search}"' })
        
        students = Student.objects.filter(profile_image_verified=False)
        return render(request, 'profile_image_unverified_list.html', {'students': students, 'student': student})
    
    except:
        return render(request, 'login.html')
  

def unlock_profile(request,id):
    student = Student.objects.get(id=id)
    viewer = Student.objects.get(email=request.session['email'])
    if viewer.role != 'Student':
        student.profile_image_verified = False
        student.save()
        return redirect('profile_image_unverified_list')
    return redirect('profile_image_unverified_list')
    

def lock_profile(request,id):
    student = Student.objects.get(id=id)
    viewer = Student.objects.get(email=request.session['email'])
    if viewer.role != 'Student':
        student.profile_image_verified = True
        student.save()
        return redirect('profile_image_unverified_list')
    return redirect('profile_image_unverified_list')

def unverified_aadhar_list(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            students = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(mobile__icontains=search) | Q(aadhar__icontains=search), aadhar_verified=False).order_by('id')
            return render(request, 'unverified_aadhar_list.html', {'students': students, 'student': student, 'msg': f'Search results for "{search}"' })
        
        students = Student.objects.filter(aadhar_verified=False)
        return render(request, 'unverified_aadhar_list.html', {'students': students, 'student': student})
    
    except:
        return render(request, 'login.html')


def verified_aadhar_list(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            students = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(mobile__icontains=search) | Q(aadhar__icontains=search), aadhar_verified=True).order_by('id')
            return render(request, 'verified_aadhar_list.html', {'students': students, 'student': student, 'msg': f'Search results for "{search}"' })
        
        students = Student.objects.filter(aadhar_verified=True)
        return render(request, 'verified_aadhar_list.html', {'students': students, 'student': student})
    
    except:
        return render(request, 'login.html')



def aadhar_mark_verified(request,id):
    student = Student.objects.get(id=id)
    viewer = Student.objects.get(email=request.session['email'])
    if viewer.role != 'Student':
        student.aadhar_verified_by = str(viewer.first_name + " " + viewer.last_name)
        student.aadhar_verified = True
        student.save()
        subject = "Greetings!!! Aadhaar Card verified Successfully"
        email_msg = aadhar_verified_msg.format(student=student,viewer=viewer)
        email_list = list(Student.objects.filter(role="Sir").values_list('email',flat=True))
        email_list.append(settings.EMAIL_HOST_USER)
        email = EmailMessage(subject, email_msg, settings.EMAIL_HOST_USER, [student.email])
        email.cc = email_list
        email.send()
        return redirect('unverified_aadhar_list')
    return redirect('unverified_aadhar_list')

def aadhar_mark_unverified(request,id):
    student = Student.objects.get(id=id)
    viewer = Student.objects.get(email=request.session['email'])
    if viewer.role != 'Student':
        student.aadhar_verified_by = str(viewer.first_name + " " + viewer.last_name)
        student.aadhar_verified = False
        student.save()
        return redirect('unverified_aadhar_list')
    return redirect('unverified_aadhar_list')

def view_student(request, id, msg=''):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        profile = Student.objects.get(id=id) 
        return render(request, 'view_student.html', {'student': student, 'profile': profile, 'msg': msg})
    except:
        return render(request, 'login.html')
    
def batch_list(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            students = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(mobile__icontains=search) | Q(batch_name__icontains=search)).order_by('batch_start_date')
            return render(request, 'batch_list.html', {'students': students, 'student': student, 'msg': f'Search results for "{search}"' })
        
        students = Student.objects.all().order_by('batch_start_date')
        return render(request, 'batch_list.html', {'students': students, 'student': student})
    
    except:
        return render(request, 'login.html')
    

def update_batch_details(request,id):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        profile = Student.objects.get(id=id) 

        if request.method == "POST":
            profile.batch_name = request.POST['batch_name']
            if request.POST['batch_start_date']:
                profile.batch_start_date = request.POST['batch_start_date']
            if request.POST['batch_end_date']:
                profile.batch_end_date = request.POST['batch_end_date']
            profile.save()

            return render(request, 'update_batch_details.html', {'student': student,'profile':profile,'msg':'Batch details updated successfully'})
        return render(request, 'update_batch_details.html', {'student': student,'profile':profile})
    except:
        return render(request, 'login.html')
    
def fees_list(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            students = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(mobile__icontains=search) | Q(fees_amount__icontains=search)).order_by('fees_status')
            return render(request, 'fees_list.html', {'students': students, 'student': student, 'msg': f'Search results for "{search}"' })
        
        students = Student.objects.all().order_by('fees_status')
        return render(request, 'fees_list.html', {'students': students, 'student': student})
    
    except:
        return render(request, 'login.html')

def update_fees_details(request,id):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        profile = Student.objects.get(id=id) 

        if request.method == "POST":
            profile.fees_amount = request.POST['fees_amount']
            profile.fees_paid = request.POST['fees_paid']
            if request.POST['fees_status'] == "True":
                profile.fees_status = True
                profile.fees_marker = f"{student.first_name} {student.last_name}"
                profile.save()
                subject = "Greetings!!! Payment Received Successfully"
                email_msg = fees_paid_msg.format(profile=profile,student=student)
                email_list = list(Student.objects.filter(role="Sir").values_list('email',flat=True))
                email_list.append(settings.EMAIL_HOST_USER)
                email = EmailMessage(subject, email_msg, settings.EMAIL_HOST_USER, [profile.email])
                email.cc = email_list
                email.send()
            else:
                profile.fees_status = False
                profile.save()

            return render(request, 'update_fees_details.html', {'student': student,'profile':profile, 'msg':"Fees Details updated Successfully"})
        return render(request, 'update_fees_details.html', {'student': student,'profile':profile})
    except:
        return render(request, 'login.html')
    

def forgot_password(request, id):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        profile = Student.objects.get(id=id)
        subject = 'Password Recovery'
        message = forgot_password_msg.format(profile=profile)
        send_mail(subject, message, settings.EMAIL_HOST_USER, [profile.email])
        return redirect('view_student', id=id, msg='Password sent to the registered email')
    except:
        return render(request, 'login.html')

def warn_unverified_students(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        students = list(Student.objects.filter(Q(verified=False) | Q(password_reset=False)).values_list('email', flat=True))
        
        subject = "Warning!!! Complete Your Account Setup"
        message = unverified_accounts_warning_msg
        send_mail(subject, message, settings.EMAIL_HOST_USER, students)
        
        return redirect('mentor-index')
    except:
        return render(request, 'login.html')
    

def delete_unverified_students(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.GET.get('Owner'):
            students = Student.objects.filter(Q(verified=False) | Q(password_reset=False))
            students.delete()
        else:
            students = Student.objects.filter(verified=False)
            students.delete()
        
        return redirect('mentor-index')
    except:
        return render(request, 'login.html')
    
def unlock_all(request):
    students = Student.objects.filter(block=True)
    students.update(block=False)
    return redirect('students_list')

def fees_reminder(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        students = list(Student.objects.filter(fees_status=False).values_list('email', flat=True))
        
        subject = "Reminder!!! Fees Payment Pending"
        email = EmailMessage(subject, fees_reminder_msg, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
        email.bcc = students
        email.send()
        
        return redirect('fees_unpaid_list')
    except:
        return render(request, 'login.html')
    
def enquiry_list(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            enquiries = Enquiry.objects.filter(Q(name__icontains=search) | Q(mobile__icontains=search)).order_by('id')
            return render(request, 'enquiry_list.html', {'enquiries':enquiries, 'student': student, 'msg': f'Search results for "{search}"' })
        
        enquiries = Enquiry.objects.all()
        return render(request, 'enquiry_list.html', {'enquiries':enquiries, 'student': student})
    
    except:
        return render(request, 'login.html')
    
def delete_enquiry(request, id):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        enquiry = Enquiry.objects.get(id=id)
        enquiry.delete()
        return redirect('enquiry_list')
    except:
        return render(request, 'login.html')

def add_event(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            title = request.POST.get('title')
            date = request.POST.get('date')
            time = request.POST.get('time')
            description = request.POST.get('description')
            day = request.POST.get('day')
            location = request.POST.get('location')
            location_link = request.POST.get('location_link')
            charges = request.POST.get('charges')
            dress_code = request.POST.get('dress_code')
            
            event = Event.objects.create(
                title=title,
                date=date,
                time=time,
                description=description,
                day=day,
                location=location,
            )

            if location_link:
                event.location_link = location_link
            if charges:
                event.charges = charges
            if dress_code:
                event.dress_code = dress_code
            event.save()
            return render(request, 'add_event.html', {'student': student, 'msg': 'Event added successfully'})
        
        return render(request, 'add_event.html', {'student': student})
    except:
        return render(request, 'login.html')

def event_list(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            events = Event.objects.filter(title__icontains=search).order_by('date')
            return render(request, 'event_list.html', {'events': events, 'student': student, 'msg': f'Search results for "{search}"' })
        
        events = Event.objects.all().order_by('date')
        return render(request, 'event_list.html', {'events': events, 'student': student})
    
    except:
        return render(request, 'login.html')

def update_event(request, id):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        event = Event.objects.get(id=id)

        if request.method == "POST":
            event.title = request.POST['title']
            if request.POST['date']:
                event.date = request.POST['date']
            if request.POST['time']:
                event.time = request.POST['time']
            event.description = request.POST['description']
            event.day = request.POST['day']
            event.location = request.POST['location']
            event.location_link = request.POST.get('location_link', '')
            event.charges = request.POST.get('charges', 0)
            event.dress_code = request.POST.get('dress_code', '')

            event.save()
            return render(request, 'update_event.html', {'student': student, 'event': event, 'msg': 'Event updated successfully'})
        
        return render(request, 'update_event.html', {'student': student, 'event': event})
    except:
        return render(request, 'login.html') 

def delete_event(request, id):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        event = Event.objects.get(id=id)
        event.delete()
        return redirect('event_list')
    except:
        return render(request, 'login.html')

def players_list(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            player = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(mobile__icontains=search) | Q(email__icontains=search)).order_by('id')
            return render(request, 'players_list.html', {'player': player, 'student': student, 'msg': f'Search results for "{search}"' })

        players = Cricket_Event.objects.all().order_by('team__name')
        cricket_teams = Cricket_Team.objects.all().order_by('name')
        return render(request, 'players_list.html', {'players': players, 'cricket_teams': cricket_teams , 'student': student})
    
    except:
        return render(request, 'login.html')

def add_cricketplayer(request, id):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        player = Student.objects.get(id=id)
        teams = Cricket_Team.objects.all().order_by('name')
        
        team_detail = None
        reg_msg = None
        try:
            team_detail = Cricket_Event.objects.get(player=player)
        except:
            reg_msg = "Player is not registered in any team"
            # return render(request, 'add_cricketplayer.html', {'student': student, 'teams': teams, 'player': player, 'reg_msg': reg_msg})
        if request.method == 'POST':
            team = Cricket_Team.objects.get(id=request.POST['team'])
            event = Event.objects.get(title__icontains=request.POST['event'])
            
            if team_detail == None:
                team_detail = Cricket_Event.objects.create(
                    player=player,
                    team=team,
                    event=event,
                    event_fees = request.POST.get('event_fees', 200),
                    fees_status = request.POST.get('fees_status', True),
                )
            else:
                team_detail.team = team
                team_detail.save()
            return redirect('players_list')
            # return render(request, 'add_cricketplayer.html', {'student': student, 'team_detail': team_detail, 'player': player, 'teams': teams , 'msg': 'Player added to team successfully'})
        return render(request, 'add_cricketplayer.html', {'student': student, 'team_detail': team_detail, 'reg_msg': reg_msg, 'teams': teams, 'player': player})    
    except:
        return render(request, 'login.html')