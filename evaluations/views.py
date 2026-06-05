"""
Module 5 — Évaluations (côté étudiant)
  - Liste enseignants filtrée par département de l'étudiant
  - Logique cours général vs spécialisé
  - Sélection enseignant → cours → formulaire
  - Soumission — une seule fois par enseignant/cours
  - Génération PDF automatique
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q

from accounts.models import User
from courses.models import Course, TeacherCourse
from questions.models import Question
from .models import Evaluation, Answer, EvaluationPdf
from .pdf_generator import generate_evaluation_pdf


# ── Decorator helper ──────────────────────────────────────────────────────────

def student_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_student():
            messages.error(request, "Accès réservé aux étudiants.")
            return redirect('home')
        if not request.user.has_completed_profile():
            messages.warning(request, "Veuillez d'abord compléter votre profil.")
            return redirect('complete_profile_student')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ── Helper ────────────────────────────────────────────────────────────────────

def _accessible_courses(profile):
    """Cours généraux OU spécialisés correspondant au profil étudiant."""
    return Course.objects.filter(
        department=profile.department,
        level=profile.level,
        is_active=True,
    ).filter(
        Q(is_general=True) |
        Q(is_general=False, specialization=profile.specialization)
    )


def _already_evaluated(student, teacher, course):
    return Evaluation.objects.filter(
        student=student, teacher=teacher, course=course, status='submitted',
    ).exists()


# ═══════════════════════════════════════════════════════════════════════════════
# VUE 1 — Liste des enseignants accessibles
# ═══════════════════════════════════════════════════════════════════════════════

@student_required
def teacher_list(request):
    profile = request.user.student_profile
    courses = _accessible_courses(profile)

    teacher_course_qs = (
        TeacherCourse.objects
        .filter(course__in=courses)
        .select_related('teacher', 'course')
    )

    teachers_map = {}
    for tc in teacher_course_qs:
        t = tc.teacher
        if t.pk not in teachers_map:
            teachers_map[t.pk] = {'teacher': t, 'courses': []}
        teachers_map[t.pk]['courses'].append(tc.course)

    result = []
    for data in teachers_map.values():
        teacher = data['teacher']
        total   = len(data['courses'])
        done    = Evaluation.objects.filter(
            student=request.user, teacher=teacher,
            course__in=data['courses'], status='submitted',
        ).count()
        result.append({
            'teacher':    teacher,
            'nb_courses': total,
            'nb_done':    done,
            'all_done':   (done == total),
        })

    result.sort(key=lambda x: x['teacher'].get_full_name() or x['teacher'].username)

    return render(request, 'evaluations/student/teacher_list.html', {
        'teachers_data': result,
        'profile':       profile,
        'page_title':    'Choisir un enseignant',
    })


# ═══════════════════════════════════════════════════════════════════════════════
# VUE 2 — Cours disponibles pour un enseignant
# ═══════════════════════════════════════════════════════════════════════════════

@student_required
def course_select(request, teacher_pk):
    profile = request.user.student_profile
    teacher = get_object_or_404(User, pk=teacher_pk, role='teacher', is_active=True)

    accessible     = _accessible_courses(profile)
    teacher_courses = (
        TeacherCourse.objects
        .filter(teacher=teacher, course__in=accessible)
        .select_related('course', 'course__level', 'course__specialization')
    )

    courses_data = []
    for tc in teacher_courses:
        courses_data.append({
            'course':    tc.course,
            'evaluated': _already_evaluated(request.user, teacher, tc.course),
        })

    if not courses_data:
        messages.info(request, "Cet enseignant n'a pas de cours accessible pour votre profil.")
        return redirect('evaluation_teacher_list')

    return render(request, 'evaluations/student/course_select.html', {
        'teacher':      teacher,
        'courses_data': courses_data,
        'page_title':   f'Évaluer {teacher.get_full_name() or teacher.username}',
    })


# ═══════════════════════════════════════════════════════════════════════════════
# VUE 3 — Formulaire d'évaluation
# ═══════════════════════════════════════════════════════════════════════════════

@student_required
def evaluation_form(request, teacher_pk, course_pk):
    profile = request.user.student_profile
    teacher = get_object_or_404(User, pk=teacher_pk, role='teacher', is_active=True)
    course  = get_object_or_404(Course, pk=course_pk, is_active=True)

    # Accès
    if not _accessible_courses(profile).filter(pk=course.pk).exists():
        messages.error(request, "Vous n'avez pas accès à ce cours.")
        return redirect('evaluation_teacher_list')

    if not TeacherCourse.objects.filter(teacher=teacher, course=course).exists():
        messages.error(request, "Cet enseignant n'enseigne pas ce cours.")
        return redirect('evaluation_course_select', teacher_pk=teacher_pk)

    # Doublon
    if _already_evaluated(request.user, teacher, course):
        messages.warning(request, "Vous avez déjà évalué cet enseignant pour ce cours.")
        return redirect('evaluation_course_select', teacher_pk=teacher_pk)

    questions = Question.objects.filter(is_active=True)

    if not questions.exists():
        messages.error(request, "Aucune question n'est disponible pour le moment.")
        return redirect('evaluation_teacher_list')

    if request.method == 'POST':
        errors = []
        for q in questions:
            if q.type == 'scored':
                val = request.POST.get(f'question_{q.pk}', '').strip()
                if not val:
                    errors.append(f'La question « {q.text[:50]}… » requiert une note.')
                elif not val.isdigit() or int(val) not in range(1, 6):
                    errors.append(f'Note invalide pour « {q.text[:50]}… » (1 à 5 attendu).')

        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, 'evaluations/student/evaluation_form.html', {
                'teacher': teacher, 'course': course, 'questions': questions,
                'page_title': f'Évaluation — {teacher.get_full_name() or teacher.username}',
                'post_data': request.POST,
            })

        with transaction.atomic():
            evaluation = Evaluation.objects.create(
                student=request.user, teacher=teacher,
                course=course, status='submitted',
            )
            for q in questions:
                if q.type == 'scored':
                    Answer.objects.create(
                        evaluation=evaluation, question=q,
                        score=int(request.POST.get(f'question_{q.pk}')),
                    )
                else:
                    text = request.POST.get(f'question_{q.pk}', '').strip()
                    Answer.objects.create(
                        evaluation=evaluation, question=q,
                        text_answer=text or None,
                    )

            # Génération PDF
            try:
                import os
                from django.conf import settings as django_settings
                filepath = generate_evaluation_pdf(evaluation)
                media_root = getattr(django_settings, 'MEDIA_ROOT',
                                     os.path.join(django_settings.BASE_DIR, 'media'))
                rel_path = os.path.relpath(filepath, media_root)
                EvaluationPdf.objects.create(evaluation=evaluation, file_path=rel_path)
            except Exception as exc:
                import logging
                logging.getLogger(__name__).error(f'PDF generation failed: {exc}')

        messages.success(request, 'Évaluation soumise avec succès !')
        return redirect('evaluation_confirmation', pk=evaluation.pk)

    return render(request, 'evaluations/student/evaluation_form.html', {
        'teacher': teacher, 'course': course, 'questions': questions,
        'page_title': f'Évaluation — {teacher.get_full_name() or teacher.username}',
        'post_data': {},
    })


# ═══════════════════════════════════════════════════════════════════════════════
# VUE 4 — Confirmation
# ═══════════════════════════════════════════════════════════════════════════════

@student_required
def evaluation_confirmation(request, pk):
    evaluation = get_object_or_404(
        Evaluation, pk=pk, student=request.user, status='submitted',
    )
    return render(request, 'evaluations/student/evaluation_confirmation.html', {
        'evaluation': evaluation,
        'page_title': 'Évaluation soumise',
    })