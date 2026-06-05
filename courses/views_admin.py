"""
Module 3 — CRUD Matieres (Cours) pour l'admin
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError

from accounts.models import Department, Specialization, Level
from .models import Course


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

    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        dept_id = request.POST.get('department', '')
        lvl_id  = request.POST.get('level', '')
        spec_id = request.POST.get('specialization', '').strip()
        is_gen  = request.POST.get('is_general') == 'on'

        ctx = {
            'page_title': 'Nouvelle matiere', 'action': 'Creer',
            'departments': departments, 'levels': levels,
            'specializations': specializations,
            'v': request.POST,
        }

        if not name or not dept_id or not lvl_id:
            messages.error(request, 'Nom, departement et niveau sont obligatoires.')
            return render(request, 'courses/admin/course_form.html', ctx)

        try:
            dept  = Department.objects.get(pk=dept_id)
            level = Level.objects.get(pk=lvl_id)
            spec  = Specialization.objects.get(pk=spec_id) if spec_id else None

            Course.objects.create(
                name=name, department=dept, level=level,
                specialization=spec, is_general=is_gen,
            )
            messages.success(request, f'Matiere « {name} » creee.')
            return redirect('course_list')
        except (Department.DoesNotExist, Level.DoesNotExist):
            messages.error(request, 'Departement ou niveau invalide.')
        except Specialization.DoesNotExist:
            messages.error(request, 'Specialisation invalide.')

    return render(request, 'courses/admin/course_form.html', {
        'page_title': 'Nouvelle matiere', 'action': 'Creer',
        'departments': departments, 'levels': levels,
        'specializations': specializations,
    })


@admin_required
def course_edit(request, pk):
    course          = get_object_or_404(Course, pk=pk)
    departments     = Department.objects.all()
    levels          = Level.objects.order_by('order')
    specializations = Specialization.objects.select_related('department').order_by('department__name', 'name')

    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        dept_id = request.POST.get('department', '')
        lvl_id  = request.POST.get('level', '')
        spec_id = request.POST.get('specialization', '').strip()
        is_gen  = request.POST.get('is_general') == 'on'

        if not name or not dept_id or not lvl_id:
            messages.error(request, 'Nom, departement et niveau sont obligatoires.')
            return render(request, 'courses/admin/course_form.html', {
                'page_title': 'Modifier matiere', 'action': 'Enregistrer',
                'departments': departments, 'levels': levels,
                'specializations': specializations, 'object': course,
                'v': request.POST,
            })

        try:
            course.name           = name
            course.department     = Department.objects.get(pk=dept_id)
            course.level          = Level.objects.get(pk=lvl_id)
            course.specialization = Specialization.objects.get(pk=spec_id) if spec_id else None
            course.is_general     = is_gen
            course.save()
            messages.success(request, f'Matiere « {name} » modifiee.')
            return redirect('course_list')
        except (Department.DoesNotExist, Level.DoesNotExist):
            messages.error(request, 'Departement ou niveau invalide.')
        except Specialization.DoesNotExist:
            messages.error(request, 'Specialisation invalide.')

    return render(request, 'courses/admin/course_form.html', {
        'page_title': 'Modifier matiere', 'action': 'Enregistrer',
        'departments': departments, 'levels': levels,
        'specializations': specializations, 'object': course,
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
