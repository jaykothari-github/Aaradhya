from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='mentor-login'),
    path('', views.index, name='mentor-index'),
    path('delete_profile/<int:id>/', views.delete_profile, name='delete_profile'),
    path('students_list/', views.students_list, name='students_list'),
    path("view_student/<int:id>/<str:msg>", views.view_student, name='view_student'),
    path("view_student/<int:id>", views.view_student, name='view_student'),
    path("forgot_password/<int:id>", views.forgot_password, name='forgot_password'),
]