from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('otp/', views.otp, name='otp'),
    # path('students/', views.student_list, name='student_list'),
    path('icard_profile', views.icard_profile, name='icard_profile'),
]