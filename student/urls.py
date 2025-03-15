from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    # path('students/', views.student_list, name='student_list'),
    # path('students/<int:id>/', views.student_detail, name='student_detail'),
]