from django.urls import path
from . import views
from . import views_results

urlpatterns = [
    # ── Flux étudiant (Module 5) ───────────────────────────────────────────────
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

    # ── Module 6 — Résultats & Classement ────────────────────────────────────

    # Classement public
    path('classement/',
         views_results.public_ranking,
         name='public_ranking'),

    # Enseignant : mes scores
    path('mes-scores/',
         views_results.teacher_scores,
         name='my_scores'),

    # Enseignant : détail matière
    path('mes-scores/teacher/<int:teacher_pk>/cours/<int:course_pk>/',
         views_results.teacher_course_detail,
         name='my_course_detail'),

    # Admin : scores d'un enseignant
    path('admin/enseignants/<int:teacher_pk>/scores/',
         views_results.admin_teacher_scores,
         name='admin_teacher_scores'),

    # Admin : détail matière d'un enseignant
    path('admin/enseignants/<int:teacher_pk>/cours/<int:course_pk>/',
         views_results.teacher_course_detail,
         name='admin_course_detail'),

    # Admin : liste toutes évaluations
    path('admin/evaluations/',
         views_results.admin_evaluation_list,
         name='admin_evaluation_list'),

    # Admin : détail d'une évaluation
    path('admin/evaluations/<int:pk>/',
         views_results.admin_evaluation_detail,
         name='admin_evaluation_detail'),

    # Admin : téléchargement PDF
    path('admin/evaluations/<int:pk>/pdf/',
         views_results.admin_download_pdf,
         name='admin_download_pdf'),
]
