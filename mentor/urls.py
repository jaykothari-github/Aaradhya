from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='mentor-login'),
    path('', views.index, name='mentor-index'),
    path('delete_profile/<int:id>/', views.delete_profile, name='delete_profile'),
]