from django.contrib import admin
from .models import *

# Register your models here.

# @admin.register(Student)
# class ModelMember(admin.ModelAdmin):
#     list_display = ['first_name', 'last_name', 'id', 'email','aadhar','verified']

@admin.action(description="Block ID cards")
def block_id(modeladmin, request, queryset):
    queryset.update(block=True)

@admin.action(description="Unblock ID cards")
def unblock_id(modeladmin, request, queryset):
    queryset.update(block=False)

class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'id', 'email','aadhar','verified']
    list_filter = ['block']
    search_fields = ['first_name', 'last_name', 'email','aadhar']
    actions = [block_id, unblock_id]

admin.site.register(Student, StudentAdmin)

admin.site.register(Enquiry)


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time']
    search_fields = ['title'] 

admin.site.register(Event, EventAdmin)

class Cricket_TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'captain', 'dress_code']
    search_fields = ['name']

admin.site.register(Cricket_Team, Cricket_TeamAdmin)

class Cricket_EventAdmin(admin.ModelAdmin):
    list_display = ['event', 'player', 'id', 'team', 'fees_status']

admin.site.register(Cricket_Event, Cricket_EventAdmin)