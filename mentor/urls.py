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
    path('fees_paid_list/', views.fees_paid_list, name='fees_paid_list'),
    path('fees_unpaid_list/', views.fees_unpaid_list, name='fees_unpaid_list'),
    path('all_verified/', views.all_verified, name='all_verified'),
    path('sir_list/', views.sir_list, name='sir_list'),
    path('profile_image_verified_list/', views.profile_image_verified_list, name='profile_image_verified_list'),
    path('profile_image_unverified_list/', views.profile_image_unverified_list, name='profile_image_unverified_list'),
    path('unlock_profile/<int:id>', views.unlock_profile, name='unlock_profile'),
    path('lock_profile/<int:id>', views.lock_profile, name='lock_profile'),
]