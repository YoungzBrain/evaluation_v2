from django.urls import path
from . import views_admin

urlpatterns = [
    # ── Module 3 : Matieres ───────────────────────────────────────────────────
    path('admin/courses/',               views_admin.course_list,   name='course_list'),
    path('admin/courses/new/',           views_admin.course_create, name='course_create'),
    path('admin/courses/<int:pk>/edit/', views_admin.course_edit,   name='course_edit'),
    path('admin/courses/<int:pk>/toggle/', views_admin.course_toggle, name='course_toggle'),
    path('admin/courses/<int:pk>/delete/', views_admin.course_delete, name='course_delete'),
]
