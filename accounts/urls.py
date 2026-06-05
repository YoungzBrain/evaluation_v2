from django.urls import path
from . import views

urlpatterns = [
    # ── Public ────────────────────────────────────────────────────────────────
    path('',                        views.home,                     name='home'),
    path('register/',               views.register,                 name='register'),
    path('login/',                  views.login_view,               name='login'),
    path('logout/',                 views.logout_view,              name='logout'),

     # ── API ───────────────────────────────────────────────────────────────────
    path('api/specializations/',      views.api_specializations,       name='api_specializations'),


    # ── Profile completion ────────────────────────────────────────────────────
    path('complete-profile/student/', views.complete_profile_student, name='complete_profile_student'),
    path('complete-profile/teacher/', views.complete_profile_teacher, name='complete_profile_teacher'),

    # ── Dashboards ────────────────────────────────────────────────────────────
    path('admin/dashboard/',        views.admin_dashboard,          name='admin_dashboard'),
    path('teacher/dashboard/',      views.teacher_dashboard,        name='teacher_dashboard'),
    path('student/dashboard/',      views.student_dashboard,        name='student_dashboard'),
    
]