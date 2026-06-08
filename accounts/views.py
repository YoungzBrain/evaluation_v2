from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, Department, Specialization, Level, StudentProfile, TeacherProfile
from courses.models import Course, TeacherCourse


# ── Public home ───────────────────────────────────────────────────────────────

def home(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)
    # Redirect to the enriched public ranking page (Module 6)
    return redirect('public_ranking')


# ── Auth ──────────────────────────────────────────────────────────────────────

def register(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip().lower()
        password   = request.POST.get('password', '')
        confirm    = request.POST.get('confirm_password', '')
        # Public registration must always create students. Teacher accounts
        # are created/managed by admins only.
        role       = 'student'

        # --- Validations ---
        if not first_name or not last_name:
            messages.error(request, 'Veuillez renseigner votre nom et prenom.')
            return render(request, 'accounts/register.html', {'role': role})

        if password != confirm:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return render(request, 'accounts/register.html', {'role': role})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Un compte avec cet email existe deja.')
            return render(request, 'accounts/register.html', {'role': role})

        # role is enforced to 'student' for public registrations

        # --- Validation du mot de passe ---
        try:
            validate_password(password)
        except ValidationError as e:
            for err in e.messages:
                messages.error(request, err)
            return render(request, 'accounts/register.html', {'role': role})

        # --- Création du compte ---
        try:
            user = User.objects.create_user(
                username   = email,   # username = email (unique)
                email      = email,
                password   = password,
                first_name = first_name,
                last_name  = last_name,
                role       = role,
            )
        except Exception as e:
            messages.error(request, f'Erreur lors de la creation du compte : {e}')
            return render(request, 'accounts/register.html', {'role': role})

        # --- Connexion automatique ---
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        messages.success(request, 'Compte cree avec succes. Completez votre profil.')

        # Public users always complete the student profile
        return redirect('complete_profile_student')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        password   = request.POST.get('password', '')

        user = None

        # Chercher par email d'abord
        try:
            user_obj = User.objects.get(email=identifier.lower())
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            pass

        # Fallback: login direct par username
        if user is None:
            user = authenticate(request, username=identifier, password=password)

        if user is not None and user.is_active:
            # Block teacher accounts from logging in via the public form.
            if getattr(user, 'role', None) == 'teacher':
                messages.error(request, 'Les comptes personnes évaluées sont gérés par l\'administration.')
            else:
                login(request, user)
                return redirect_by_role(user)
        else:
            messages.error(request, 'Identifiant ou mot de passe incorrect.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ── Profile completion ────────────────────────────────────────────────────────

@login_required
def complete_profile_student(request):
    if request.user.role != 'student':
        return redirect_by_role(request.user)

    # Profil déjà complété → dashboard
    if hasattr(request.user, 'student_profile'):
        return redirect('student_dashboard')

    departments = Department.objects.all()
    levels      = Level.objects.all().order_by('order')

    if request.method == 'POST':
        dept_id  = request.POST.get('department', '').strip()
        level_id = request.POST.get('level', '').strip()
        spec_id  = request.POST.get('specialization', '').strip()

        ctx = {'departments': departments, 'levels': levels,
               'sel_dept': dept_id, 'sel_level': level_id, 'sel_spec': spec_id}

        if not dept_id or not level_id:
            messages.error(request, 'Veuillez choisir un departement et un niveau.')
            return render(request, 'accounts/complete_profile_student.html', ctx)

        # La spécialisation est optionnelle si le département n'en a pas
        has_specs = Specialization.objects.filter(department_id=dept_id).exists()
        if has_specs and not spec_id:
            messages.error(request, 'Veuillez choisir une specialisation.')
            return render(request, 'accounts/complete_profile_student.html', ctx)

        # Vérifications FK
        try:
            dept  = Department.objects.get(pk=dept_id)
            level = Level.objects.get(pk=level_id)
        except (Department.DoesNotExist, Level.DoesNotExist):
            messages.error(request, 'Departement ou niveau invalide.')
            return render(request, 'accounts/complete_profile_student.html', ctx)

        spec = None
        if spec_id:
            try:
                spec = Specialization.objects.get(pk=spec_id, department=dept)
            except Specialization.DoesNotExist:
                messages.error(request, 'Specialisation invalide pour ce departement.')
                return render(request, 'accounts/complete_profile_student.html', ctx)

        StudentProfile.objects.create(
            user           = request.user,
            department     = dept,
            level          = level,
            specialization = spec,
        )

        messages.success(request, 'Profil complete avec succes. Bienvenue !')
        return redirect('student_dashboard')

    return render(request, 'accounts/complete_profile_student.html', {
        'departments': departments,
        'levels':      levels,
    })


@login_required
def complete_profile_teacher(request):
    if request.user.role != 'teacher':
        return redirect_by_role(request.user)

    if hasattr(request.user, 'teacher_profile'):
        return redirect('teacher_dashboard')

    departments = Department.objects.all()
    levels      = Level.objects.all().order_by('order')
    courses     = Course.objects.filter(is_active=True).select_related('department', 'level')

    if request.method == 'POST':
        dept_ids   = request.POST.getlist('departments')
        course_ids = request.POST.getlist('courses')

        if not dept_ids:
            messages.error(request, 'Veuillez selectionner au moins un departement.')
            return render(request, 'accounts/complete_profile_teacher.html', {
                'departments': departments, 'levels': levels, 'courses': courses,
                'sel_depts': dept_ids, 'sel_courses': course_ids,
            })

        profile = TeacherProfile.objects.create(user=request.user)
        profile.departments.set(dept_ids)

        for course_id in course_ids:
            try:
                course = Course.objects.get(pk=course_id)
                TeacherCourse.objects.get_or_create(
                    teacher=request.user,
                    course=course
                )
            except Course.DoesNotExist:
                pass

        messages.success(request, 'Profil complete avec succes. Bienvenue !')
        return redirect('teacher_dashboard')

    return render(request, 'accounts/complete_profile_teacher.html', {
        'departments': departments,
        'levels':      levels,
        'courses':     courses,
    })


# ── Dashboards ────────────────────────────────────────────────────────────────

@login_required
def admin_dashboard(request):
    if not request.user.is_admin():
        return redirect_by_role(request.user)

    from evaluations.models import Evaluation
    total_teachers      = User.objects.filter(role='teacher').count()
    total_students      = User.objects.filter(role='student').count()
    total_courses       = Course.objects.count()
    total_departments   = Department.objects.count()
    total_evaluations   = Evaluation.objects.filter(status='submitted').count()

    departments = Department.objects.all()
    courses     = Course.objects.filter(is_active=True).select_related('department', 'level')

    return render(request, 'accounts/admin_dashboard.html', {
        'total_teachers':    total_teachers,
        'total_students':    total_students,
        'total_courses':     total_courses,
        'total_departments': total_departments,
        'total_evaluations': total_evaluations,
        'departments':       departments,
        'courses':           courses,
    })


@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher():
        return redirect_by_role(request.user)

    if not request.user.has_completed_profile():
        return redirect('complete_profile_teacher')

    return render(request, 'accounts/teacher_dashboard.html')


@login_required
def student_dashboard(request):
    if not request.user.is_student():
        return redirect_by_role(request.user)

    if not request.user.has_completed_profile():
        return redirect('complete_profile_student')

    return render(request, 'accounts/student_dashboard.html')


# ── Helper ────────────────────────────────────────────────────────────────────

def redirect_by_role(user):
    if user.role == 'admin':
        return redirect('admin_dashboard')
    if not user.has_completed_profile():
        if user.role == 'student':
            return redirect('complete_profile_student')
        elif user.role == 'teacher':
            return redirect('complete_profile_teacher')
    if user.role == 'teacher':
        return redirect('teacher_dashboard')
    return redirect('student_dashboard')


# ── API ───────────────────────────────────────────────────────────────────────

def api_specializations(request):
    dept_id = request.GET.get('department')
    if not dept_id:
        return JsonResponse([], safe=False)
    specs = Specialization.objects.filter(department_id=dept_id).values('id', 'name')
    return JsonResponse(list(specs), safe=False)
