from django.urls import path
from . import views

urlpatterns = [
    # ── Flux étudiant ─────────────────────────────────────────────────────────
    path('evaluate/',
         views.teacher_list,
         name='evaluation_teacher_list'),

    path('evaluate/teacher/<int:teacher_pk>/courses/',
         views.course_select,
         name='evaluation_course_select'),

    path('evaluate/teacher/<int:teacher_pk>/course/<int:course_pk>/',
         views.evaluation_form,
         name='evaluation_form'),

    path('evaluate/confirmation/<int:pk>/',
         views.evaluation_confirmation,
         name='evaluation_confirmation'),
]