from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import User, Department, Specialization, Level, StudentProfile, TeacherProfile
from courses.models import Course, TeacherCourse


# ── Public home ───────────────────────────────────────────────────────────────

def home(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)
    departments = Department.objects.all()
    return render(request, 'accounts/home.html', {'departments': departments})


# ── Auth ──────────────────────────────────────────────────────────────────────

def register(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip()
        password   = request.POST.get('password', '')
        confirm    = request.POST.get('confirm_password', '')
        role       = request.POST.get('role', 'student')

        if password != confirm:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Un compte avec cet email existe deja.')
            return render(request, 'accounts/register.html')

        if role not in ['student', 'teacher']:
            messages.error(request, 'Role invalide.')
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(
            username   = email,
            email      = email,
            password   = password,
            first_name = first_name,
            last_name  = last_name,
            role       = role,
        )

        login(request, user)
        messages.success(request, 'Compte cree avec succes. Completez votre profil.')

        if role == 'student':
            return redirect('complete_profile_student')
        else:
            return redirect('complete_profile_teacher')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        password   = request.POST.get('password', '')

        user = None

        try:
            user_obj = User.objects.get(email=identifier)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            pass

        if user is None:
            user = authenticate(request, username=identifier, password=password)

        if user is not None and user.is_active:
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

    if hasattr(request.user, 'student_profile'):
        return redirect('student_dashboard')

    departments = Department.objects.all()
    levels      = Level.objects.all()

    if request.method == 'POST':
        dept_id  = request.POST.get('department')
        level_id = request.POST.get('level')
        spec_id  = request.POST.get('specialization')

        print("dept:", dept_id)
        print("level:", level_id)
        print("spec:", spec_id)

        if not dept_id or not level_id or not spec_id:
            messages.error(request, 'Veuillez remplir tous les champs.')
            return render(request, 'accounts/complete_profile_student.html', {
                'departments': departments, 'levels': levels
            })

        StudentProfile.objects.create(
            user              = request.user,
            department_id     = dept_id,
            level_id          = level_id,
            specialization_id = spec_id,
        )

        messages.success(request, 'Profil complete avec succes.')
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
    levels      = Level.objects.all()
    courses     = Course.objects.filter(is_active=True)

    if request.method == 'POST':
        dept_ids = request.POST.getlist('departments')

        if not dept_ids:
            messages.error(request, 'Veuillez selectionner au moins un departement.')
            return render(request, 'accounts/complete_profile_teacher.html', {
                'departments': departments, 'levels': levels, 'courses': courses
            })

        profile = TeacherProfile.objects.create(user=request.user)
        profile.departments.set(dept_ids)

        course_ids = request.POST.getlist('courses')
        for course_id in course_ids:
            try:
                course = Course.objects.get(pk=course_id)
                TeacherCourse.objects.get_or_create(
                    teacher=request.user,
                    course=course
                )
            except Course.DoesNotExist:
                pass

        messages.success(request, 'Profil complete avec succes.')
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

    total_teachers    = User.objects.filter(role='teacher').count()
    total_students    = User.objects.filter(role='student').count()
    total_courses     = Course.objects.count()
    total_departments = Department.objects.count()

    return render(request, 'accounts/admin_dashboard.html', {
        'total_teachers':    total_teachers,
        'total_students':    total_students,
        'total_courses':     total_courses,
        'total_departments': total_departments,
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
    if not user.has_completed_profile():
        if user.role == 'student':
            return redirect('complete_profile_student')
        elif user.role == 'teacher':
            return redirect('complete_profile_teacher')
    if user.role == 'admin':
        return redirect('admin_dashboard')
    elif user.role == 'teacher':
        return redirect('teacher_dashboard')
    else:
        return redirect('student_dashboard')


# ── API ───────────────────────────────────────────────────────────────────────

def api_specializations(request):
    dept_id = request.GET.get('department')
    if not dept_id:
        return JsonResponse([], safe=False)
    specs = Specialization.objects.filter(department_id=dept_id).values('id', 'name')
    return JsonResponse(list(specs), safe=False)