
from django.urls import path
from . import views
from . import views_admin

urlpatterns = [
    # ── Public ────────────────────────────────────────────────────────────────
    path('',                        views.home,                     name='home'),
    path('register/',               views.register,                 name='register'),
    path('login/',                  views.login_view,               name='login'),
    path('logout/',                 views.logout_view,              name='logout'),

    # ── API ───────────────────────────────────────────────────────────────────
    path('api/specializations/',    views.api_specializations,      name='api_specializations'),

    # ── Profile completion ────────────────────────────────────────────────────
    path('complete-profile/student/', views.complete_profile_student, name='complete_profile_student'),
    path('complete-profile/teacher/', views.complete_profile_teacher, name='complete_profile_teacher'),

    # ── Dashboards ────────────────────────────────────────────────────────────
    path('admin/dashboard/',        views.admin_dashboard,          name='admin_dashboard'),
    path('teacher/dashboard/',      views.teacher_dashboard,        name='teacher_dashboard'),
    path('student/dashboard/',      views.student_dashboard,        name='student_dashboard'),

    # ── Module 3 : Departements ───────────────────────────────────────────────
    path('admin/departments/',              views_admin.department_list,   name='department_list'),
    path('admin/departments/new/',          views_admin.department_create, name='department_create'),
    path('admin/departments/<int:pk>/edit/', views_admin.department_edit,  name='department_edit'),
    path('admin/departments/<int:pk>/delete/', views_admin.department_delete, name='department_delete'),

    # ── Module 3 : Specialisations ────────────────────────────────────────────
    path('admin/specializations/',                   views_admin.specialization_list,   name='specialization_list'),
    path('admin/specializations/new/',               views_admin.specialization_create, name='specialization_create'),
    path('admin/specializations/<int:pk>/edit/',     views_admin.specialization_edit,   name='specialization_edit'),
    path('admin/specializations/<int:pk>/delete/',   views_admin.specialization_delete, name='specialization_delete'),

    # ── Module 3 : Niveaux ────────────────────────────────────────────────────
    path('admin/levels/',               views_admin.level_list,   name='level_list'),
    path('admin/levels/new/',           views_admin.level_create, name='level_create'),
    path('admin/levels/<int:pk>/edit/', views_admin.level_edit,   name='level_edit'),
    path('admin/levels/<int:pk>/delete/', views_admin.level_delete, name='level_delete'),

    # ── Module 3 : Enseignants ────────────────────────────────────────────────
    path('admin/teachers/',                  views_admin.teacher_list,   name='teacher_list'),
    path('admin/teachers/<int:pk>/toggle/',  views_admin.teacher_toggle, name='teacher_toggle'),
]
