from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Dept, Class, Student, Attendance, Teacher, Assign, AttendanceTotal, time_slots, Week_days, AssignTime, AttendanceClass, StudentClasses, Marks, MarksClass
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
	return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

@login_required()
def attendance(request, stud_id):
    stud = Student.objects.get(sno=stud_id)
    ass_list = Assign.objects.filter(class_id_id=stud.class_id)
    att_list = []   
    for ass in ass_list:
        try:
            a = AttendanceTotal.objects.get(student=stud, class_id=ass.class_id)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=stud, class_id=ass.class_id)
            a.save()
        att_list.append(a)
    return render(request, 'attendance.html', {'att_list': att_list})

@login_required()
def attendance_detail(request, stud_id, class_id):
    stud = get_object_or_404(Student, sno=stud_id)
    cr = get_object_or_404(Class, id=class_id)
    att_list = Attendance.objects.filter(class_id=cr, student=stud).order_by('date')
    return render(request, 'attendance_detail.html', {'att_list': att_list, 'cr': cr})

@login_required()
def teacher_attendance(request, ass_c_id):
	assc = get_object_or_404(AttendanceClass, id=ass_c_id)
	ass = assc.assign
	c = ass.class_id
	context = {
		'ass': ass,
		'c': c,
		'assc': assc,
	}
	return render(request, 'teacher_attendance.html', context)

@login_required()
def teacher_class(request, teacher_id, choice):
    teacher1 = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'teacher_class.html', {'teacher1': teacher1, 'choice': choice})

@login_required()
def my_students(request, assign_id):
    ass = Assign.objects.get(id=assign_id)
    att_list = []
    for stud in ass.class_id.student_set.all():
        try:
            a = AttendanceTotal.objects.get(student=stud, class_id=ass.class_id)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=stud, class_id=ass.class_id)
            a.save()
        att_list.append(a)
    return render(request, 'my_students.html', {'att_list': att_list})

@login_required()
def edit_attendance(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    cr = assc.assign.class_id
    att_list = Attendance.objects.filter(attendanceclass=assc, class_id=cr)
    context = {
        'assc': assc,
        'att_list': att_list,
    }
    return render(request, 'teacher_edit_attendance.html', context)

@login_required()
def confirm(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    ass = assc.assign
    cr = ass.dept
    cl = ass.class_id
    for i, s in enumerate(cl.student_set.all()):
        status = request.POST[s.sno]
        if status == 'present':
            status = 'True'
        else:
            status = 'False'
        if assc.status == 1:
            try:
                a = Attendance.objects.get(class_id=cl, student=s, date=assc.date, attendanceclass=assc)
                a.status = status
                a.save()
            except Attendance.DoesNotExist:
                a = Attendance(class_id=cl, student=s, status=status, date=assc.date, attendanceclass=assc)
                a.save()
        else:
            a = Attendance(class_id=cl, student=s, status=status, date=assc.date, attendanceclass=assc)
            a.save()
            assc.status = 1
            assc.save()

    return HttpResponseRedirect(reverse('teacher_class_date', args=(ass.id,)))

@login_required()
def teacher_attendance_detail(request, stud_id, class_id):
    stud = get_object_or_404(Student, sno=stud_id)
    cr = get_object_or_404(Class, id=class_id)
    att_list = Attendance.objects.filter(class_id=cr, student=stud).order_by('date')
    return render(request, 'teacher_attendance_detail.html', {'att_list': att_list, 'cr': cr})

@login_required()
def cancel_class(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    assc.status = 2
    assc.save()
    return HttpResponseRedirect(reverse('teacher_class_date', args=(assc.assign_id,)))

@login_required()
def teacher_class_date(request, assign_id):
    now = timezone.now()
    ass = get_object_or_404(Assign, id=assign_id)
    att_list = ass.attendanceclass_set.filter(date__lte=now).order_by('-date')
    return render(request, 'teacher_class_date.html', {'att_list': att_list})

@login_required()
def teacher_marks_list(request, assign_id):
    ass = get_object_or_404(Assign, id=assign_id)
    m_list = MarksClass.objects.filter(assign=ass)
    return render(request, 'teacher_marks_list.html', {'m_list': m_list})

@login_required()
def teacher_marks_entry(request, marks_c_id):
    mc = get_object_or_404(MarksClass, id=marks_c_id)
    ass = mc.assign
    c = ass.class_id
    context = {
        'ass': ass,
        'c': c,
        'mc': mc,
    }
    return render(request, 'teacher_marks_entry.html', context)

@login_required()
def marks_list(request, stud_id):
    stud = Student.objects.get(sno=stud_id,)
    ass_list = Assign.objects.filter(class_id_id=stud.class_id)
    sc_list = []
    for ass in ass_list:
        try:
            sc = StudentClasses.objects.get(student=stud, class_id=ass.class_id)
        except StudentClasses.DoesNotExist:
            sc = StudentClasses(student=stud, class_id=ass.class_id)
            sc.save()
            sc.marks_set.create(name='Prelims exam')
            sc.marks_set.create(name='Final exam')
            sc.marks_set.create(name='Assignment')
        sc_list.append(sc)

    return render(request, 'marks_list.html', {'sc_list': sc_list})


@login_required()
def marks_confirm(request, marks_c_id):
    mc = get_object_or_404(MarksClass, id=marks_c_id)
    ass = mc.assign
    cr = ass.class_id
    # cr = Class.objects.get(std=self.class_id)
    cl = ass.class_id
    for s in cl.student_set.all():
        mark = request.POST[s.sno]
        sc = StudentClasses.objects.get(class_id=cr, student=s)
        m = sc.marks_set.get(name=mc.name)
        m.marks1 = mark
        m.save()
    mc.status = True
    mc.save()

    return HttpResponseRedirect(reverse('teacher_student_marks', args=(ass.id,)))

@login_required()
def edit_marks(request, marks_c_id):
    mc = get_object_or_404(MarksClass, id=marks_c_id)
    cr = mc.assign.class_id
    stud_list = mc.assign.class_id.student_set.all()
    m_list = []
    for stud in stud_list:
        sc = StudentClasses.objects.get(class_id=cr, student=stud)
        m = sc.marks_set.get(name=mc.name)
        m_list.append(m)
    context = {
        'mc': mc,
        'm_list': m_list,
    }
    return render(request, 'edit_marks.html', context)

@login_required()
def student_marks(request, assign_id):
    ass = Assign.objects.get(id=assign_id)
    sc_list = StudentClasses.objects.filter(student__in=ass.class_id.student_set.all(), class_id=ass.class_id)
    return render(request, 'teacher_student_marks.html', {'sc_list': sc_list})
