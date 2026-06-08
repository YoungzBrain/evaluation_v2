"""
Module 3 — Gestion Academique (Admin)
  - CRUD Departements
  - CRUD Specialisations
  - CRUD Niveaux
  - Desactivation / reactivation enseignants
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError

from .models import User, Department, Specialization, Level, TeacherProfile
from courses.models import Course, TeacherCourse


# ── Decorator helper ──────────────────────────────────────────────────────────

def admin_required(view_func):
    """Redirige vers le dashboard si l'utilisateur n'est pas admin."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin():
            messages.error(request, "Acces reserve a l'administrateur.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ═══════════════════════════════════════════════════════════════════════════════
# DÉPARTEMENTS
# ═══════════════════════════════════════════════════════════════════════════════

@admin_required
def department_list(request):
    departments = Department.objects.prefetch_related('specializations').order_by('name')
    return render(request, 'accounts/admin/department_list.html', {
        'departments': departments,
        'page_title': 'Departements',
    })


@admin_required
def department_create(request):
    if request.method == 'POST':
        name        = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        if not name:
            messages.error(request, 'Le nom du departement est obligatoire.')
            return render(request, 'accounts/admin/department_form.html', {
                'page_title': 'Nouveau departement', 'action': 'Creer',
            })

        try:
            Department.objects.create(name=name, description=description or None)
            messages.success(request, f'Departement « {name} » cree avec succes.')
            return redirect('department_list')
        except IntegrityError:
            messages.error(request, 'Un departement avec ce nom existe deja.')

    return render(request, 'accounts/admin/department_form.html', {
        'page_title': 'Nouveau departement', 'action': 'Creer',
    })


@admin_required
def department_edit(request, pk):
    dept = get_object_or_404(Department, pk=pk)

    if request.method == 'POST':
        name        = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        if not name:
            messages.error(request, 'Le nom du departement est obligatoire.')
            return render(request, 'accounts/admin/department_form.html', {
                'page_title': 'Modifier departement', 'action': 'Enregistrer',
                'object': dept,
            })

        try:
            dept.name        = name
            dept.description = description or None
            dept.save()
            messages.success(request, f'Departement « {name} » modifie.')
            return redirect('department_list')
        except IntegrityError:
            messages.error(request, 'Un departement avec ce nom existe deja.')

    return render(request, 'accounts/admin/department_form.html', {
        'page_title': 'Modifier departement', 'action': 'Enregistrer',
        'object': dept,
    })


@admin_required
def department_delete(request, pk):
    dept = get_object_or_404(Department, pk=pk)

    if request.method == 'POST':
        name = dept.name
        try:
            dept.delete()
            messages.success(request, f'Departement « {name} » supprime.')
        except Exception:
            messages.error(request, 'Impossible de supprimer ce departement car des donnees y sont liees.')
        return redirect('department_list')

    return render(request, 'accounts/admin/confirm_delete.html', {
        'page_title': 'Supprimer departement',
        'object_name': dept.name,
        'object_type': 'departement',
        'cancel_url': 'department_list',
    })


# ═══════════════════════════════════════════════════════════════════════════════
# SPÉCIALISATIONS
# ═══════════════════════════════════════════════════════════════════════════════

@admin_required
def specialization_list(request):
    dept_filter = request.GET.get('department', '')
    specs = Specialization.objects.select_related('department').order_by('department__name', 'name')
    departments = Department.objects.all()

    if dept_filter:
        specs = specs.filter(department_id=dept_filter)

    return render(request, 'accounts/admin/specialization_list.html', {
        'specializations': specs,
        'departments': departments,
        'dept_filter': dept_filter,
        'page_title': 'Specialisations',
    })


@admin_required
def specialization_create(request):
    departments = Department.objects.all()

    if request.method == 'POST':
        name        = request.POST.get('name', '').strip()
        dept_id     = request.POST.get('department', '')
        description = request.POST.get('description', '').strip()

        if not name or not dept_id:
            messages.error(request, 'Le nom et le departement sont obligatoires.')
            return render(request, 'accounts/admin/specialization_form.html', {
                'page_title': 'Nouvelle specialisation', 'action': 'Creer',
                'departments': departments,
            })

        try:
            dept = Department.objects.get(pk=dept_id)
            Specialization.objects.create(
                name=name, department=dept, description=description or None
            )
            messages.success(request, f'Specialisation « {name} » creee.')
            return redirect('specialization_list')
        except Department.DoesNotExist:
            messages.error(request, 'Departement invalide.')
        except IntegrityError:
            messages.error(request, 'Cette specialisation existe deja dans ce departement.')

    return render(request, 'accounts/admin/specialization_form.html', {
        'page_title': 'Nouvelle specialisation', 'action': 'Creer',
        'departments': departments,
    })


@admin_required
def specialization_edit(request, pk):
    spec        = get_object_or_404(Specialization, pk=pk)
    departments = Department.objects.all()

    if request.method == 'POST':
        name        = request.POST.get('name', '').strip()
        dept_id     = request.POST.get('department', '')
        description = request.POST.get('description', '').strip()

        if not name or not dept_id:
            messages.error(request, 'Le nom et le departement sont obligatoires.')
            return render(request, 'accounts/admin/specialization_form.html', {
                'page_title': 'Modifier specialisation', 'action': 'Enregistrer',
                'departments': departments, 'object': spec,
            })

        try:
            spec.name        = name
            spec.department  = Department.objects.get(pk=dept_id)
            spec.description = description or None
            spec.save()
            messages.success(request, f'Specialisation « {name} » modifiee.')
            return redirect('specialization_list')
        except Department.DoesNotExist:
            messages.error(request, 'Departement invalide.')
        except IntegrityError:
            messages.error(request, 'Cette specialisation existe deja dans ce departement.')

    return render(request, 'accounts/admin/specialization_form.html', {
        'page_title': 'Modifier specialisation', 'action': 'Enregistrer',
        'departments': departments, 'object': spec,
    })


@admin_required
def specialization_delete(request, pk):
    spec = get_object_or_404(Specialization, pk=pk)

    if request.method == 'POST':
        name = spec.name
        try:
            spec.delete()
            messages.success(request, f'Specialisation « {name} » supprimee.')
        except Exception:
            messages.error(request, 'Impossible de supprimer : des etudiants ou cours utilisent cette specialisation.')
        return redirect('specialization_list')

    return render(request, 'accounts/admin/confirm_delete.html', {
        'page_title': 'Supprimer specialisation',
        'object_name': f'{spec.name} ({spec.department})',
        'object_type': 'specialisation',
        'cancel_url': 'specialization_list',
    })


# ═══════════════════════════════════════════════════════════════════════════════
# NIVEAUX
# ═══════════════════════════════════════════════════════════════════════════════

@admin_required
def level_list(request):
    levels = Level.objects.order_by('order')
    return render(request, 'accounts/admin/level_list.html', {
        'levels': levels,
        'page_title': 'Niveaux',
    })


@admin_required
def level_create(request):
    if request.method == 'POST':
        name  = request.POST.get('name', '').strip()
        order = request.POST.get('order', '0').strip()

        if not name:
            messages.error(request, 'Le nom du niveau est obligatoire.')
            return render(request, 'accounts/admin/level_form.html', {
                'page_title': 'Nouveau niveau', 'action': 'Creer',
            })

        try:
            Level.objects.create(name=name, order=int(order))
            messages.success(request, f'Niveau « {name} » cree.')
            return redirect('level_list')
        except IntegrityError:
            messages.error(request, 'Un niveau avec ce nom existe deja.')
        except ValueError:
            messages.error(request, "L'ordre doit etre un nombre entier.")

    return render(request, 'accounts/admin/level_form.html', {
        'page_title': 'Nouveau niveau', 'action': 'Creer',
    })


@admin_required
def level_edit(request, pk):
    level = get_object_or_404(Level, pk=pk)

    if request.method == 'POST':
        name  = request.POST.get('name', '').strip()
        order = request.POST.get('order', '0').strip()

        if not name:
            messages.error(request, 'Le nom du niveau est obligatoire.')
            return render(request, 'accounts/admin/level_form.html', {
                'page_title': 'Modifier niveau', 'action': 'Enregistrer', 'object': level,
            })

        try:
            level.name  = name
            level.order = int(order)
            level.save()
            messages.success(request, f'Niveau « {name} » modifie.')
            return redirect('level_list')
        except IntegrityError:
            messages.error(request, 'Un niveau avec ce nom existe deja.')
        except ValueError:
            messages.error(request, "L'ordre doit etre un nombre entier.")

    return render(request, 'accounts/admin/level_form.html', {
        'page_title': 'Modifier niveau', 'action': 'Enregistrer', 'object': level,
    })


@admin_required
def level_delete(request, pk):
    level = get_object_or_404(Level, pk=pk)

    if request.method == 'POST':
        name = level.name
        try:
            level.delete()
            messages.success(request, f'Niveau « {name} » supprime.')
        except Exception:
            messages.error(request, 'Impossible de supprimer : des etudiants ou cours utilisent ce niveau.')
        return redirect('level_list')

    return render(request, 'accounts/admin/confirm_delete.html', {
        'page_title': 'Supprimer niveau',
        'object_name': level.name,
        'object_type': 'niveau',
        'cancel_url': 'level_list',
    })


# ═══════════════════════════════════════════════════════════════════════════════
# GESTION DES PERSONNES ÉVALUÉES
# ═══════════════════════════════════════════════════════════════════════════════

@admin_required
def teacher_list(request):
    teachers = (
        User.objects
        .filter(role='teacher')
        .prefetch_related('teacher_profile__departments', 'teacher_courses__course')
        .order_by('last_name', 'first_name')
    )
    departments = Department.objects.all()
    courses = Course.objects.select_related('department', 'level').filter(is_active=True).order_by('department__name', 'level__order', 'name')

    return render(request, 'accounts/admin/teacher_list.html', {
        'teachers': teachers,
        'departments': departments,
        'courses': courses,
        'page_title': 'Personnes évaluées',
    })


@admin_required
def teacher_toggle(request, pk):
    """Active ou desactive un compte de personne évaluée."""
    teacher = get_object_or_404(User, pk=pk, role='teacher')

    if request.method == 'POST':
        teacher.is_active = not teacher.is_active
        teacher.save()
        status = 'active' if teacher.is_active else 'desactive'
        messages.success(request, f'Compte de {teacher.get_full_name()} {status}.')
    return redirect('teacher_list')


@admin_required
def teacher_edit(request, pk):
    teacher = get_object_or_404(User, pk=pk, role='teacher')
    departments = Department.objects.all()
    courses = Course.objects.select_related('department', 'level').filter(is_active=True).order_by('department__name', 'level__order', 'name')
    profile = getattr(teacher, 'teacher_profile', None)

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip().lower()
        dept_ids   = request.POST.getlist('departments')
        course_ids = request.POST.getlist('courses')

        if not first_name or not last_name or not email:
            messages.error(request, 'Veuillez renseigner le nom, prenom et email.')
            return render(request, 'accounts/admin/teacher_form.html', {
                'teacher': teacher,
                'departments': departments,
                'courses': courses,
                'selected_department_ids': set(int(d) for d in dept_ids if d.isdigit()),
                'selected_course_ids': set(int(c) for c in course_ids if c.isdigit()),
                'page_title': 'Modifier enseignant',
                'action': 'Enregistrer',
            })

        if User.objects.exclude(pk=teacher.pk).filter(email=email).exists():
            messages.error(request, 'Un compte avec cet email existe deja.')
            return render(request, 'accounts/admin/teacher_form.html', {
                'teacher': teacher,
                'departments': departments,
                'courses': courses,
                'selected_department_ids': set(int(d) for d in dept_ids if d.isdigit()),
                'selected_course_ids': set(int(c) for c in course_ids if c.isdigit()),
                'page_title': 'Modifier enseignant',
                'action': 'Enregistrer',
            })

        teacher.first_name = first_name
        teacher.last_name = last_name
        teacher.email = email
        teacher.username = email
        teacher.save()

        if not profile:
            profile = TeacherProfile.objects.create(user=teacher)

        profile.departments.set(dept_ids)

        selected_course_ids = set(int(c) for c in course_ids if c.isdigit())
        existing_course_ids = set(teacher.teacher_courses.values_list('course_id', flat=True))

        for removed_id in existing_course_ids - selected_course_ids:
            TeacherCourse.objects.filter(teacher=teacher, course_id=removed_id).delete()

        for course_id in selected_course_ids - existing_course_ids:
            try:
                course = Course.objects.get(pk=course_id)
                TeacherCourse.objects.get_or_create(teacher=teacher, course=course)
            except Course.DoesNotExist:
                continue

        messages.success(request, 'Enseignant modifie avec succes.')
        return redirect('teacher_list')

    selected_department_ids = set(profile.departments.values_list('id', flat=True)) if profile else set()
    selected_course_ids = set(teacher.teacher_courses.values_list('course_id', flat=True))

    return render(request, 'accounts/admin/teacher_form.html', {
        'teacher': teacher,
        'departments': departments,
        'courses': courses,
        'selected_department_ids': selected_department_ids,
        'selected_course_ids': selected_course_ids,
        'page_title': 'Modifier enseignant',
        'action': 'Enregistrer',
    })


@admin_required
def teacher_create(request):
    """Create a teacher account (admin only). Assign departments and courses."""
    departments = Department.objects.all()
    courses = Course.objects.select_related('department', 'level').filter(is_active=True).order_by('department__name', 'level__order', 'name')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip().lower()
        dept_ids   = request.POST.getlist('departments')
        course_ids = request.POST.getlist('courses')

        if not first_name or not last_name or not email:
            messages.error(request, 'Veuillez renseigner le nom, prenom et email.')
            return render(request, 'accounts/admin/teacher_form.html', {
                'teacher': None,
                'departments': departments,
                'courses': courses,
                'selected_department_ids': set(int(d) for d in dept_ids if d.isdigit()),
                'selected_course_ids': set(int(c) for c in course_ids if c.isdigit()),
                'page_title': 'Nouvel évalué',
                'action': 'Créer',
            })

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Un compte avec cet email existe deja.')
            return render(request, 'accounts/admin/teacher_form.html', {
                'teacher': None,
                'departments': departments,
                'courses': courses,
                'selected_department_ids': set(int(d) for d in dept_ids if d.isdigit()),
                'selected_course_ids': set(int(c) for c in course_ids if c.isdigit()),
                'page_title': 'Nouvel évalué',
                'action': 'Créer',
            })

        try:
            user = User.objects.create_user(
                username = email,
                email    = email,
                password = None,
                first_name = first_name,
                last_name  = last_name,
                role = 'teacher',
                is_active = True,
            )
            # Ensure teacher cannot login with a password
            user.set_unusable_password()
            user.save()

            profile = getattr(user, 'teacher_profile', None)
            if not profile:
                profile = TeacherProfile.objects.create(user=user)

            if dept_ids:
                profile.departments.set(dept_ids)

            current_course_ids = set()
            for course_id in course_ids:
                try:
                    course = Course.objects.get(pk=course_id)
                    TeacherCourse.objects.get_or_create(teacher=user, course=course)
                    current_course_ids.add(course.id)
                except Course.DoesNotExist:
                    continue

            messages.success(request, 'Compte enseignant cree avec succes.')
            return redirect('teacher_list')
        except Exception as e:
            messages.error(request, f'Erreur lors de la creation du compte: {e}')
            return render(request, 'accounts/admin/teacher_form.html', {
                'teacher': None,
                'departments': departments,
                'courses': courses,
                'selected_department_ids': set(int(d) for d in dept_ids if d.isdigit()),
                'selected_course_ids': set(int(c) for c in course_ids if c.isdigit()),
                'page_title': 'Nouvel évalué',
                'action': 'Créer',
            })

    return render(request, 'accounts/admin/teacher_form.html', {
        'teacher': None,
        'departments': departments,
        'courses': courses,
        'selected_department_ids': set(),
        'selected_course_ids': set(),
        'page_title': 'Nouvel évalué',
        'action': 'Créer',
    })
