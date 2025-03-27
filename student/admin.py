from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Student)
class ModelMember(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'id', 'email','aadhar','verified']