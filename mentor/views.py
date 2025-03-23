from django.shortcuts import render
from student.models import Student

# Create your views here.

def login(request):
    return render(request, 'login.html')

def index(request):
    try:
        student = Student.objects.get(email=request.session['email'])
        if student.role == 'Student':
            return render(request, 'login.html', {'msg': 'You are not authorized to access this page'})
        
        students = Student.objects.all()
        return render(request, 'index.html', {'students': students, 'student': student})
    except:
        return render(request, 'login.html')