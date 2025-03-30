from django.shortcuts import render
from student.models import Student
from django.db.models import Q
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from student.messages import forgot_password_msg

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
    # try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        students = Student.objects.all()
        students_count = students.count() 
        fees_pending = students.filter(fees_status=False).count()
        pending_verification = students.filter( Q(profile_image_verified=False) | Q(aadhar_verified=False)).exclude(verified=False).order_by('created_at')[:8]
        all_verified = students.filter(fees_status=True, verified=True, password_reset=True, profile_image_verified=True, aadhar_verified=True ).count() 
        unverified_list = students.filter(Q(verified=False) | Q(password_reset=False)).order_by('created_at')
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
    # except:
    #     return render(request, 'login.html')


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
            students = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(mobile__icontains=search) | Q(aadhar__icontains=search)).order_by('id')
            return render(request, 'students_list.html', {'students': students, 'student': student, 'msg': f'Search results for "{search}"' })
        
        students = Student.objects.all()
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
    # try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            students = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(mobile__icontains=search) | Q(aadhar__icontains=search), profile_image_verified=False).order_by('id')
            return render(request, 'profile_image_unverified_list.html', {'students': students, 'student': student, 'msg': f'Search results for "{search}"' })
        
        students = Student.objects.filter(profile_image_verified=False)
        return render(request, 'profile_image_unverified_list.html', {'students': students, 'student': student})
    
    # except:
    #     return render(request, 'login.html')
  

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
    # try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            students = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(mobile__icontains=search) | Q(aadhar__icontains=search), aadhar_verified=False).order_by('id')
            return render(request, 'unverified_aadhar_list.html', {'students': students, 'student': student, 'msg': f'Search results for "{search}"' })
        
        students = Student.objects.filter(aadhar_verified=False)
        return render(request, 'unverified_aadhar_list.html', {'students': students, 'student': student})
    
    # except:
    #     return render(request, 'login.html')


def verified_aadhar_list(request):
    # try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        if request.method == 'POST':
            search = request.POST.get('search')
            students = Student.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(mobile__icontains=search) | Q(aadhar__icontains=search), aadhar_verified=True).order_by('id')
            return render(request, 'verified_aadhar_list.html', {'students': students, 'student': student, 'msg': f'Search results for "{search}"' })
        
        students = Student.objects.filter(aadhar_verified=True)
        return render(request, 'verified_aadhar_list.html', {'students': students, 'student': student})
    
    # except:
    #     return render(request, 'login.html')



def aadhar_mark_verified(request,id):
    student = Student.objects.get(id=id)
    viewer = Student.objects.get(email=request.session['email'])
    if viewer.role != 'Student':
        student.aadhar_verified_by = str(viewer.first_name + " " + viewer.last_name)
        student.aadhar_verified = True
        student.save()
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

        return render(request, 'update_batch_details.html', {'student': student,'profile':profile})
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
        # return render(request, 'view_student.html', {'student': student, 'profile': profile, 'msg': 'Password sent to the registered email'})
        return redirect('view_student', id=id, msg='Password sent to the registered email')
    except:
        return render(request, 'login.html')
