"""
Module 3 — CRUD Matieres (Cours) pour l'admin
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError

from accounts.models import Department, Specialization, Level, User
from .models import Course, TeacherCourse


def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin():
            messages.error(request, "Acces reserve a l'administrateur.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@admin_required
def course_list(request):
    dept_filter = request.GET.get('department', '')
    courses = (
        Course.objects
        .select_related('department', 'level', 'specialization')
        .order_by('department__name', 'level__order', 'name')
    )
    departments = Department.objects.all()

    if dept_filter:
        courses = courses.filter(department_id=dept_filter)

    return render(request, 'courses/admin/course_list.html', {
        'courses': courses,
        'departments': departments,
        'dept_filter': dept_filter,
        'page_title': 'Matieres',
    })


@admin_required
def course_create(request):
    departments     = Department.objects.all()
    levels          = Level.objects.order_by('order')
    specializations = Specialization.objects.select_related('department').order_by('department__name', 'name')
    teachers        = User.objects.filter(role='teacher', is_active=True).order_by('last_name', 'first_name')

    if request.method == 'POST':
        name        = request.POST.get('name', '').strip()
        dept_id     = request.POST.get('department', '')
        lvl_id      = request.POST.get('level', '')
        spec_id     = request.POST.get('specialization', '').strip()
        is_gen      = request.POST.get('is_general') == 'on'
        teacher_ids = request.POST.getlist('teachers')
        selected_teacher_ids = set(int(tid) for tid in teacher_ids if tid.isdigit())

        ctx = {
            'page_title': 'Nouvelle matiere', 'action': 'Creer',
            'departments': departments, 'levels': levels,
            'specializations': specializations, 'teachers': teachers,
            'v': request.POST,
            'selected_teacher_ids': selected_teacher_ids,
        }

        if not name or not dept_id or not lvl_id:
            messages.error(request, 'Nom, departement et niveau sont obligatoires.')
            return render(request, 'courses/admin/course_form.html', ctx)

        try:
            dept  = Department.objects.get(pk=dept_id)
            level = Level.objects.get(pk=lvl_id)
            spec  = Specialization.objects.get(pk=spec_id) if spec_id else None

            course = Course.objects.create(
                name=name, department=dept, level=level,
                specialization=spec, is_general=is_gen,
            )
            for teacher_id in teacher_ids:
                try:
                    teacher = User.objects.get(pk=teacher_id, role='teacher')
                    TeacherCourse.objects.get_or_create(teacher=teacher, course=course)
                except User.DoesNotExist:
                    continue
            messages.success(request, f'Matiere « {name} » creee.')
            return redirect('course_list')
        except (Department.DoesNotExist, Level.DoesNotExist):
            messages.error(request, 'Departement ou niveau invalide.')
        except Specialization.DoesNotExist:
            messages.error(request, 'Specialisation invalide.')

    return render(request, 'courses/admin/course_form.html', {
        'page_title': 'Nouvelle matiere', 'action': 'Creer',
        'departments': departments, 'levels': levels,
        'specializations': specializations, 'teachers': teachers,
        'selected_teacher_ids': set(),
        'assigned_teacher_ids': set(),
    })


@admin_required
def course_edit(request, pk):
    course          = get_object_or_404(Course, pk=pk)
    departments     = Department.objects.all()
    levels          = Level.objects.order_by('order')
    specializations = Specialization.objects.select_related('department').order_by('department__name', 'name')
    teachers        = User.objects.filter(role='teacher', is_active=True).order_by('last_name', 'first_name')

    if request.method == 'POST':
        name        = request.POST.get('name', '').strip()
        dept_id     = request.POST.get('department', '')
        lvl_id      = request.POST.get('level', '')
        spec_id     = request.POST.get('specialization', '').strip()
        is_gen      = request.POST.get('is_general') == 'on'
        teacher_ids = request.POST.getlist('teachers')

        if not name or not dept_id or not lvl_id:
            messages.error(request, 'Nom, departement et niveau sont obligatoires.')
            assigned_teacher_ids = set(course.teacher_courses.values_list('teacher_id', flat=True))
            return render(request, 'courses/admin/course_form.html', {
                'page_title': 'Modifier matiere', 'action': 'Enregistrer',
                'departments': departments, 'levels': levels,
                'specializations': specializations, 'teachers': teachers,
                'object': course,
                'v': request.POST,
                'selected_teacher_ids': set(int(tid) for tid in teacher_ids if tid.isdigit()),
                'assigned_teacher_ids': assigned_teacher_ids,
            })

        try:
            course.name           = name
            course.department     = Department.objects.get(pk=dept_id)
            course.level          = Level.objects.get(pk=lvl_id)
            course.specialization = Specialization.objects.get(pk=spec_id) if spec_id else None
            course.is_general     = is_gen
            course.save()

            selected_teacher_ids = set(int(tid) for tid in teacher_ids if tid.isdigit())
            existing_teacher_ids = set(course.teacher_courses.values_list('teacher_id', flat=True))

            # remove old assignments not currently selected
            for removed_id in existing_teacher_ids - selected_teacher_ids:
                TeacherCourse.objects.filter(teacher_id=removed_id, course=course).delete()

            # add new assignments
            for teacher_id in selected_teacher_ids - existing_teacher_ids:
                try:
                    teacher = User.objects.get(pk=teacher_id, role='teacher')
                    TeacherCourse.objects.get_or_create(teacher=teacher, course=course)
                except User.DoesNotExist:
                    continue

            messages.success(request, f'Matiere « {name} » modifiee.')
            return redirect('course_list')
        except (Department.DoesNotExist, Level.DoesNotExist):
            messages.error(request, 'Departement ou niveau invalide.')
        except Specialization.DoesNotExist:
            messages.error(request, 'Specialisation invalide.')

    assigned_teacher_ids = set(course.teacher_courses.values_list('teacher_id', flat=True))
    return render(request, 'courses/admin/course_form.html', {
        'page_title': 'Modifier matiere', 'action': 'Enregistrer',
        'departments': departments, 'levels': levels,
        'specializations': specializations, 'teachers': teachers,
        'object': course,
        'selected_teacher_ids': set(),
        'assigned_teacher_ids': assigned_teacher_ids,
    })


@admin_required
def course_toggle(request, pk):
    """Active ou desactive une matiere."""
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.is_active = not course.is_active
        course.save()
        status = 'activee' if course.is_active else 'desactivee'
        messages.success(request, f'Matiere « {course.name} » {status}.')
    return redirect('course_list')


@admin_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        name = course.name
        try:
            course.delete()
            messages.success(request, f'Matiere « {name} » supprimee.')
        except Exception:
            messages.error(request, 'Impossible de supprimer : des evaluations utilisent cette matiere.')
        return redirect('course_list')

    return render(request, 'accounts/admin/confirm_delete.html', {
        'page_title': 'Supprimer matiere',
        'object_name': course.name,
        'object_type': 'matiere',
        'cancel_url': 'course_list',
    })
