from django.contrib import admin

from . models import Dept, Class, Student, Attendance, Teacher, Assign, AssignTime, AttendanceClass
from . models import AttendanceTotal, StudentClasses, Marks, MarksClass, User
from django.contrib.auth.admin import UserAdmin

class StudentInline(admin.TabularInline):
    model = Student
    extra = 0

class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'dept', 'std')
    search_fields = ('id', 'dept__name', 'std')
    ordering = ['dept__name', 'std']
    inlines = [StudentInline]

class MarksInline(admin.TabularInline):
    model = Marks
    extra = 0

class StudentClassesAdmin(admin.ModelAdmin):
    inlines = [MarksInline]
    list_display = ('student', 'class_id',)
    search_fields = ('student__name', 'student__class_id__id', 'student__class_id__dept__name')
    ordering = ('student__class_id__dept__name', 'student__class_id__id', 'student__sno')

class AssignTimeInline(admin.TabularInline):
	model = AssignTime
	extra = 0

class AssignAdmin(admin.ModelAdmin):
    inlines = [AssignTimeInline]
    list_display = ('class_id', 'dept', 'teacher')
    search_fields = ('class_id__id', 'dept__name', 'teacher__name')
    ordering = ['class_id__dept__name', 'class_id__id']
    raw_id_fields = ['class_id', 'dept', 'teacher']

admin.site.register(User, UserAdmin)
admin.site.register(Dept)
admin.site.register(Class, ClassAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Assign, AssignAdmin)
admin.site.register(StudentClasses, StudentClassesAdmin)