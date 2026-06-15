"""
Module 4 — Gestion des Questions (Admin)
  - CRUD Questions
  - Activation / désactivation questions
  - Import CSV en masse
  - Rapport d'import
"""
import csv
import io
import os
import tempfile

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.conf import settings

from .models import Question


# ── Decorator helper ──────────────────────────────────────────────────────────

def admin_required(view_func):
    """Redirige vers home si l'utilisateur n'est pas admin."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin():
            messages.error(request, "Accès réservé à l'administrateur.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ═══════════════════════════════════════════════════════════════════════════════
# LISTE
# ═══════════════════════════════════════════════════════════════════════════════

@admin_required
def question_list(request):
    filter_type   = request.GET.get('type', '')
    filter_status = request.GET.get('status', '')

    qs = Question.objects.all()

    if filter_type in ('scored', 'open'):
        qs = qs.filter(type=filter_type)

    if filter_status == 'active':
        qs = qs.filter(is_active=True)
    elif filter_status == 'inactive':
        qs = qs.filter(is_active=False)

    return render(request, 'questions/admin/question_list.html', {
        'questions':      qs,
        'filter_type':    filter_type,
        'filter_status':  filter_status,
        'page_title':     'Questions d\'évaluation',
        'total':          Question.objects.count(),
        'active_count':   Question.objects.filter(is_active=True).count(),
        'scored_count':   Question.objects.filter(type='scored').count(),
        'open_count':     Question.objects.filter(type='open').count(),
    })


# ═══════════════════════════════════════════════════════════════════════════════
# CREATE
# ═══════════════════════════════════════════════════════════════════════════════

@admin_required
def question_create(request):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        qtype = request.POST.get('type', 'scored')
        is_active = request.POST.get('is_active') == 'on'

        if not text:
            messages.error(request, 'Le texte de la question est obligatoire.')
            return render(request, 'questions/admin/question_form.html', {
                'page_title': 'Nouvelle question', 'action': 'Créer',
                'form_data': {'text': text, 'type': qtype, 'is_active': is_active},
            })

        Question.objects.create(text=text, type=qtype, is_active=is_active)
        messages.success(request, 'Question créée avec succès.')
        return redirect('question_list')

    return render(request, 'questions/admin/question_form.html', {
        'page_title': 'Nouvelle question', 'action': 'Créer',
        'form_data': {'type': 'scored', 'is_active': True},
    })


# ═══════════════════════════════════════════════════════════════════════════════
# EDIT
# ═══════════════════════════════════════════════════════════════════════════════

@admin_required
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.method == 'POST':
        text      = request.POST.get('text', '').strip()
        qtype     = request.POST.get('type', 'scored')
        is_active = request.POST.get('is_active') == 'on'

        if not text:
            messages.error(request, 'Le texte de la question est obligatoire.')
            return render(request, 'questions/admin/question_form.html', {
                'page_title': 'Modifier la question', 'action': 'Enregistrer',
                'object': question,
                'form_data': {'text': text, 'type': qtype, 'is_active': is_active},
            })

        question.text      = text
        question.type      = qtype
        question.is_active = is_active
        question.save()
        messages.success(request, 'Question mise à jour.')
        return redirect('question_list')

    return render(request, 'questions/admin/question_form.html', {
        'page_title': 'Modifier la question', 'action': 'Enregistrer',
        'object': question,
        'form_data': {
            'text': question.text,
            'type': question.type,
            'is_active': question.is_active,
        },
    })


# ═══════════════════════════════════════════════════════════════════════════════
# DELETE
# ═══════════════════════════════════════════════════════════════════════════════

@admin_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question supprimée.')
        return redirect('question_list')

    return render(request, 'questions/admin/question_confirm_delete.html', {
        'page_title':   'Supprimer la question',
        'object':       question,
        'object_type':  'question',
        'object_name':  question.text[:60] + ('…' if len(question.text) > 60 else ''),
        'cancel_url':   'question_list',
    })


# ═══════════════════════════════════════════════════════════════════════════════
# TOGGLE actif / inactif
# ═══════════════════════════════════════════════════════════════════════════════

@admin_required
def question_toggle(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.is_active = not question.is_active
    question.save()
    state = 'activée' if question.is_active else 'désactivée'
    messages.success(request, f'Question {state}.')
    return redirect('question_list')


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT CSV
# ═══════════════════════════════════════════════════════════════════════════════

EXPECTED_HEADERS = {'text', 'type'}   # 'is_active' is optional

@admin_required
def question_import(request):
    """
    Format CSV attendu :
        text,type,is_active
        "Ma question ?",scored,1
        "Commentaire libre",open,1

    - 'type'      : 'scored' ou 'open'  (défaut : scored)
    - 'is_active' : 0 / 1  (défaut : 1)
    """
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')

        if not csv_file:
            messages.error(request, 'Veuillez sélectionner un fichier CSV.')
            return render(request, 'questions/admin/question_import.html', {
                'page_title': 'Import CSV',
            })

        if not csv_file.name.lower().endswith('.csv'):
            messages.error(request, 'Le fichier doit être au format .csv')
            return render(request, 'questions/admin/question_import.html', {
                'page_title': 'Import CSV',
            })

        # Decode + parse
        try:
            raw = csv_file.read().decode('utf-8-sig')  # utf-8-sig strips BOM
        except UnicodeDecodeError:
            messages.error(request, 'Encodage non supporté — utilisez UTF-8.')
            return render(request, 'questions/admin/question_import.html', {
                'page_title': 'Import CSV',
            })

        # Save CSV to temp file for PDF generation
        csv_temp = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8')
        csv_temp.write(raw)
        csv_temp.close()

        reader   = csv.DictReader(io.StringIO(raw))
        headers  = set(h.strip().lower() for h in (reader.fieldnames or []))

        if 'text' not in headers:
            messages.error(request, "Colonne 'text' manquante dans le CSV.")
            return render(request, 'questions/admin/question_import.html', {
                'page_title': 'Import CSV',
            })

        results = []   # {'row': n, 'text': ..., 'status': 'ok'|'error', 'reason': ...}
        created = 0
        skipped = 0

        for row_num, row in enumerate(reader, start=2):   # start=2 : ligne 1 = headers
            text  = (row.get('text') or '').strip()
            qtype = (row.get('type') or 'scored').strip().lower()
            raw_active = (row.get('is_active') or '1').strip()

            # Validation
            if not text:
                results.append({'row': row_num, 'text': '(vide)', 'status': 'error',
                                 'reason': 'Texte vide'})
                skipped += 1
                continue

            if qtype not in ('scored', 'open'):
                results.append({'row': row_num, 'text': text[:60], 'status': 'error',
                                 'reason': f"Type invalide : « {qtype} » (attendu : scored ou open)"})
                skipped += 1
                continue

            is_active = raw_active not in ('0', 'false', 'non', 'no', 'False')

            # Duplicate check (même texte exact)
            if Question.objects.filter(text=text).exists():
                results.append({'row': row_num, 'text': text[:60], 'status': 'error',
                                 'reason': 'Question identique déjà existante'})
                skipped += 1
                continue

            Question.objects.create(text=text, type=qtype, is_active=is_active)
            results.append({'row': row_num, 'text': text[:60], 'status': 'ok', 'reason': ''})
            created += 1

        # Generate PDF for display and link questions to it
        if created > 0:
            try:
                from evaluations.pdf_converter import csv_to_pdf
                from .models import PDFUpload

                pdf_path = csv_to_pdf(csv_temp.name)
                # Use the uploaded CSV filename (csv_file) to name the generated PDF
                pdf_record = PDFUpload.objects.create(
                    original_filename=f"{csv_file.name.rsplit('.', 1)[0]}.pdf",
                    uploaded_by=request.user if hasattr(request, 'user') and request.user.is_authenticated else None
                )
                pdf_record.file.name = os.path.relpath(pdf_path, getattr(settings, 'MEDIA_ROOT', os.path.join(settings.BASE_DIR, 'media')))
                pdf_record.save()

                # Link created questions to the PDF
                for idx, question in enumerate(Question.objects.filter(is_active=True).order_by('-created_at')[:created], 1):
                    question.source_pdf = pdf_record
                    question.pdf_page = 1
                    question.position = idx
                    question.save()
            except Exception as exc:
                messages.warning(request, f'PDF généré mais liaison échouée : {exc}')

        # Clean up temp file
        try:
            os.unlink(csv_temp.name)
        except Exception:
            pass

        return render(request, 'questions/admin/question_import_report.html', {
            'page_title': 'Rapport d\'import CSV',
            'results':    results,
            'created':    created,
            'skipped':    skipped,
            'total':      created + skipped,
        })

    return render(request, 'questions/admin/question_import.html', {
        'page_title': 'Import CSV',
    })