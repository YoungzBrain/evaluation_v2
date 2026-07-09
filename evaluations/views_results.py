"""
Module 6 — Résultats & Classement
    - Scores par matière (moyenne/100)
    - Détail par matière
    - Classement public dynamique
    - Toutes les évaluations (admin)
    - Détail évaluation (admin)
    - Téléchargement PDF (admin)
"""
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.http import FileResponse, Http404

from django.conf import settings as django_settings
from accounts.models import User, Department
from courses.models import Course
from questions.models import Question
from .models import Evaluation, Answer, EvaluationPdf


# ── Helpers ───────────────────────────────────────────────────────────────────

def _require_admin(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin():
            messages.error(request, "Accès réservé aux administrateurs.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def _require_teacher_or_admin(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_admin() or request.user.is_teacher()):
            messages.error(request, "Accès non autorisé.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def _score_to_100(avg_on_5):
    """Convert average on 5 → score on 100."""
    if avg_on_5 is None:
        return None
    return round(avg_on_5 * 20, 1)


def _get_teacher_scores(teacher, department=None):
    """
    Returns a list of dicts:
      { course, nb_evaluations, avg_score (on 5), score_100, score_color }
    and the global average on 100.
    
    If department is provided, only include courses from that department.
    """
    # All submitted evaluations for this teacher
    query = Evaluation.objects.filter(teacher=teacher, status='submitted')
    
    if department:
        query = query.filter(course__department=department)
    
    evaluations = query.select_related('course')

    courses_seen = {}
    for ev in evaluations:
        cid = ev.course_id
        if cid not in courses_seen:
            courses_seen[cid] = {'course': ev.course, 'evals': []}
        courses_seen[cid]['evals'].append(ev.pk)

    course_scores = []
    for cid, data in courses_seen.items():
        eval_pks = data['evals']
        scored_answers = Answer.objects.filter(
            evaluation_id__in=eval_pks,
            question__type='scored',
            score__isnull=False,
        )
        agg = scored_answers.aggregate(avg=Avg('score'))
        avg5 = agg['avg']
        s100 = _score_to_100(avg5)
        course_scores.append({
            'course':          data['course'],
            'nb_evaluations':  len(eval_pks),
            'avg_score':       round(avg5, 2) if avg5 else None,
            'score_100':       s100,
            'score_color':     _color_for_score(s100),
        })

    course_scores.sort(key=lambda x: x['score_100'] or 0, reverse=True)

    # Global average
    if course_scores:
        valid = [c['score_100'] for c in course_scores if c['score_100'] is not None]
        global_avg = round(sum(valid) / len(valid), 1) if valid else None
    else:
        global_avg = None

    return course_scores, global_avg


def _color_for_score(score):
    if score is None:
        return 'muted'
    if score >= 75:
        return 'green'
    if score >= 50:
        return 'amber'
    return 'red'


# ═══════════════════════════════════════════════════════════════════════════════
# VUE — Scores d'une personne évaluée (accessible à l'intervenant lui-même + admin)
# ═══════════════════════════════════════════════════════════════════════════════

@_require_teacher_or_admin
def teacher_scores(request, teacher_pk=None):
    """
    If teacher_pk is given (admin viewing any teacher), use it.
    If not, the logged-in teacher views their own scores.
    """
    if teacher_pk:
        if not request.user.is_admin():
            messages.error(request, "Accès réservé aux administrateurs.")
            return redirect('my_scores')
        teacher = get_object_or_404(User, pk=teacher_pk, role='teacher')
    else:
        teacher = request.user
        if not teacher.is_teacher():
            return redirect('home')

    course_scores, global_avg = _get_teacher_scores(teacher)

    return render(request, 'evaluations/results/teacher_scores.html', {
        'page_title':    f'Scores — {teacher.get_full_name() or teacher.username}',
        'teacher':       teacher,
        'course_scores': course_scores,
        'global_avg':    global_avg,
        'global_color':  _color_for_score(global_avg),
        'is_own':        (teacher == request.user),
    })


# ═══════════════════════════════════════════════════════════════════════════════
# VUE — Détail par matière (réponses texte + stats question par question)
# ═══════════════════════════════════════════════════════════════════════════════

@_require_teacher_or_admin
def teacher_course_detail(request, teacher_pk, course_pk):
    if not request.user.is_admin() and request.user.pk != teacher_pk:
        messages.error(request, "Accès non autorisé.")
        return redirect('my_scores')

    teacher = get_object_or_404(User, pk=teacher_pk, role='teacher')
    course  = get_object_or_404(Course, pk=course_pk)

    evaluations = Evaluation.objects.filter(
        teacher=teacher, course=course, status='submitted'
    ).prefetch_related('answers__question')

    if not evaluations.exists():
        messages.info(request, "Aucune évaluation pour ce cours.")
        if request.user.is_admin():
            return redirect('admin_teacher_scores', teacher_pk=teacher_pk)
        return redirect('my_scores')

    # Per-question stats
    questions = Question.objects.filter(is_active=True)
    question_stats = []
    for q in questions:
        if q.type == 'scored':
            answers = Answer.objects.filter(
                evaluation__in=evaluations, question=q, score__isnull=False
            )
            agg = answers.aggregate(avg=Avg('score'), count=Count('score'))
            dist = {i: 0 for i in range(1, 6)}
            for a in answers:
                if a.score in dist:
                    dist[a.score] += 1
            question_stats.append({
                'question':    q,
                'avg':         round(agg['avg'], 2) if agg['avg'] else None,
                'score_100':   _score_to_100(agg['avg']),
                'count':       agg['count'],
                'distribution': dist,
                'color':       _color_for_score(_score_to_100(agg['avg'])),
            })
        else:
            # Open questions: gather non-empty text answers
            open_answers = Answer.objects.filter(
                evaluation__in=evaluations,
                question=q,
                text_answer__isnull=False,
            ).exclude(text_answer='')
            question_stats.append({
                'question':    q,
                'open_answers': list(open_answers.values_list('text_answer', flat=True)),
            })

    return render(request, 'evaluations/results/course_detail.html', {
        'page_title':      f'{course.name} — {teacher.get_full_name() or teacher.username}',
        'teacher':         teacher,
        'course':          course,
        'evaluations':     evaluations,
        'question_stats':  question_stats,
        'nb_evaluations':  evaluations.count(),
        'is_own':          (teacher == request.user),
    })


# ═══════════════════════════════════════════════════════════════════════════════
# VUE — Classement public dynamique (home enrichie)
# ═══════════════════════════════════════════════════════════════════════════════

def public_ranking(request):
    """
    Public page: teachers ranked by global average score per department.
    Replaces or enriches the existing home view.
    """
    dept_filter = request.GET.get('dept')
    departments = Department.objects.all()

    ranking_data = []
    for dept in departments:
        # Teachers who have at least 1 submitted evaluation in this department
        # Find teachers via their course evaluations (not just department profile).
        teachers_with_evals = User.objects.filter(
            role='teacher',
            is_active=True,
            evaluations_as_teacher__course__department=dept,
            evaluations_as_teacher__status='submitted',
        ).distinct()

        teacher_list = []
        for t in teachers_with_evals:
            _, global_avg = _get_teacher_scores(t, department=dept)
            if global_avg is not None:
                # Subject breakdown
                course_scores_raw, _ = _get_teacher_scores(t, department=dept)
                subjects = [
                    {'name': cs['course'].name, 'score': cs['score_100']}
                    for cs in course_scores_raw if cs['score_100'] is not None
                ]
                teacher_list.append({
                    'teacher':    t,
                    'global_avg': global_avg,
                    'color':      _color_for_score(global_avg),
                    'subjects':   subjects,
                })

        teacher_list.sort(key=lambda x: x['global_avg'], reverse=True)
        ranking_data.append({
            'department':   dept,
            'teachers':     teacher_list,
            'active':       str(dept.pk) == dept_filter,
        })

    return render(request, 'evaluations/results/public_ranking.html', {
        'page_title':    'Classement public',
        'ranking_data':  ranking_data,
        'departments':   departments,
        'dept_filter':   dept_filter,
    })


# ═══════════════════════════════════════════════════════════════════════════════
# VUE ADMIN — Liste de toutes les évaluations
# ═══════════════════════════════════════════════════════════════════════════════

@_require_admin
def admin_evaluation_list(request):
    qs = Evaluation.objects.filter(status='submitted').select_related(
        'student', 'teacher', 'course', 'course__department'
    )

    # Filters
    dept_filter    = request.GET.get('dept', '')
    teacher_filter = request.GET.get('teacher', '')
    search         = request.GET.get('q', '').strip()

    if dept_filter:
        qs = qs.filter(course__department_id=dept_filter)
    if teacher_filter:
        qs = qs.filter(teacher_id=teacher_filter)
    if search:
        qs = qs.filter(
            Q(teacher__first_name__icontains=search) |
            Q(teacher__last_name__icontains=search) |
            Q(student__first_name__icontains=search) |
            Q(student__last_name__icontains=search) |
            Q(course__name__icontains=search)
        )

    departments = Department.objects.all()
    teachers    = User.objects.filter(role='teacher', is_active=True).order_by('last_name')

    return render(request, 'evaluations/admin/evaluation_list.html', {
        'page_title':    'Toutes les évaluations',
        'evaluations':   qs,
        'departments':   departments,
        'teachers':      teachers,
        'dept_filter':   dept_filter,
        'teacher_filter': teacher_filter,
        'search':        search,
        'total':         qs.count(),
    })


# ═══════════════════════════════════════════════════════════════════════════════
# VUE ADMIN — Détail d'une évaluation
# ═══════════════════════════════════════════════════════════════════════════════

@_require_admin
def admin_evaluation_detail(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk, status='submitted')
    answers    = evaluation.answers.select_related('question').order_by('question__id')

    scored_answers = [a for a in answers if a.question.type == 'scored']
    open_answers   = [a for a in answers if a.question.type == 'open']

    # Global score for this evaluation
    scores = [a.score for a in scored_answers if a.score is not None]
    avg5   = sum(scores) / len(scores) if scores else None
    s100   = _score_to_100(avg5)

    return render(request, 'evaluations/admin/evaluation_detail.html', {
        'page_title':     f'Évaluation #{evaluation.pk}',
        'evaluation':     evaluation,
        'scored_answers': scored_answers,
        'open_answers':   open_answers,
        'avg5':           round(avg5, 2) if avg5 else None,
        'score_100':      s100,
        'score_color':    _color_for_score(s100),
    })


# ═══════════════════════════════════════════════════════════════════════════════
# VUE ADMIN — Téléchargement PDF
# ═══════════════════════════════════════════════════════════════════════════════

@_require_admin
def admin_download_pdf(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk, status='submitted')

    try:
        pdf_record = evaluation.pdf
    except EvaluationPdf.DoesNotExist:
        # Try to regenerate
        try:
            from .pdf_generator import generate_evaluation_pdf
            media_root = getattr(django_settings, 'MEDIA_ROOT',
                                 os.path.join(django_settings.BASE_DIR, 'media'))
            filepath   = generate_evaluation_pdf(evaluation)
            rel_path   = os.path.relpath(filepath, media_root)
            pdf_record = EvaluationPdf.objects.create(
                evaluation=evaluation, file_path=rel_path
            )
        except Exception as exc:
            messages.error(request, f"Impossible de générer le PDF : {exc}")
            return redirect('admin_evaluation_detail', pk=pk)

    media_root = getattr(django_settings, 'MEDIA_ROOT',
                         os.path.join(django_settings.BASE_DIR, 'media'))
    full_path  = os.path.join(media_root, pdf_record.file_path)

    if not os.path.exists(full_path):
        # File missing on disk — regenerate
        try:
            from .pdf_generator import generate_evaluation_pdf
            filepath   = generate_evaluation_pdf(evaluation)
            rel_path   = os.path.relpath(filepath, media_root)
            pdf_record.file_path = rel_path
            pdf_record.save()
            full_path = filepath
        except Exception as exc:
            messages.error(request, f"Fichier PDF introuvable et régénération échouée : {exc}")
            return redirect('admin_evaluation_detail', pk=pk)

    response = FileResponse(
        open(full_path, 'rb'),
        content_type='application/pdf',
    )
    filename = f"evaluation_{evaluation.pk}_{evaluation.teacher.last_name}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


# ═══════════════════════════════════════════════════════════════════════════════
# VUE ADMIN — Scores d'une personne évaluée (depuis panel admin)
# ═══════════════════════════════════════════════════════════════════════════════

@_require_admin
def admin_teacher_scores(request, teacher_pk):
    return teacher_scores(request, teacher_pk=teacher_pk)
