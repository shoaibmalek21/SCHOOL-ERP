from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about.html', views.about, name='about'),
    path('student/<slug:stud_id>/attendance/', views.attendance, name='attendance'),
    path('student/<slug:stud_id>/<slug:class_id>/attendance/', views.attendance_detail, name='attendance_detail'),
    path('teacher/<slug:teacher_id>/<int:choice>/Classes/', views.teacher_class, name='teacher_class'),
    path('teacher/<int:assign_id>/Students/attendance/', views.my_students, name='my_students'),
    path('teacher/<int:assign_id>/ClassDates/', views.teacher_class_date, name='teacher_class_date'),
    path('teacher/<int:ass_c_id>/attendance/', views.teacher_attendance, name='teacher_attendance'),
    path('teacher/<int:ass_c_id>/Edit_attendance/', views.edit_attendance, name='edit_attendance'),
    path('teacher/<slug:stud_id>/<slug:class_id>/attendance/', views.teacher_attendance_detail, name='teacher_attendance_detail'),
    path('teacher/<int:ass_c_id>/Cancel/', views.cancel_class, name='cancel_class'),
    path('teacher/<int:ass_c_id>/attendance/confirm/', views.confirm, name='confirm'),
    path('student/<slug:stud_id>/marks_list/', views.marks_list, name='marks_list'),
    path('teacher/<int:assign_id>/marks_list/', views.teacher_marks_list, name='teacher_marks_list'),
	path('teacher/<int:marks_c_id>/marks_entry/', views.teacher_marks_entry, name='teacher_marks_entry'),
    path('teacher/<int:marks_c_id>/marks_entry/confirm/', views.marks_confirm, name='marks_confirm'),
    path('teacher/<int:marks_c_id>/Edit_marks/', views.edit_marks, name='edit_marks'),
    path('teacher/<int:assign_id>/Students/Marks/', views.student_marks, name='teacher_student_marks'),
]
