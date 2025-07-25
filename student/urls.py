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
    path('icard/', views.icard, name='icard'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('profile/', views.profile, name='profile'),
    path('student_event_list/', views.student_event_list, name='student_event_list'),
    path('event_id_card/<int:id>', views.event_id_card, name='event_id_card'),
    path('enquiry/', views.enquiry, name='enquiry'),
]