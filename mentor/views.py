from django.shortcuts import render
from student.models import Student
from django.db.models import Q
from django.shortcuts import redirect

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