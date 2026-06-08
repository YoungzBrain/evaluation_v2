"""
Génération PDF d'une évaluation soumise — ReportLab.
Produit un fichier dans media/evaluations_pdf/<id>_<timestamp>.pdf
"""
import os
from datetime import datetime

from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT


# ── Palette (cohérente avec le dark-UI) ──────────────────────────────────────
INDIGO      = colors.HexColor('#6366f1')
SLATE_DARK  = colors.HexColor('#0f172a')
SLATE_MED   = colors.HexColor('#1e293b')
SLATE_BORDER= colors.HexColor('#334155')
TEXT_MAIN   = colors.HexColor('#1e293b')
TEXT_MUTED  = colors.HexColor('#64748b')
GREEN       = colors.HexColor('#10b981')
AMBER       = colors.HexColor('#f59e0b')
RED         = colors.HexColor('#ef4444')


def _score_color(score):
    if score is None:
        return TEXT_MUTED
    if score >= 4:
        return GREEN
    if score == 3:
        return AMBER
    return RED


def _stars(score):
    """Return '★★★☆☆' style string."""
    if score is None:
        return '—'
    filled = '★' * score
    empty  = '☆' * (5 - score)
    return filled + empty


def generate_evaluation_pdf(evaluation):
    """
    Génère le PDF pour `evaluation` (instance Evaluation avec answers préchargées).
    Retourne le chemin absolu du fichier créé.
    """
    # ── Destination ──────────────────────────────────────────────────────────
    media_root = getattr(settings, 'MEDIA_ROOT', os.path.join(settings.BASE_DIR, 'media'))
    pdf_dir    = os.path.join(media_root, 'evaluations_pdf')
    os.makedirs(pdf_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename  = f'eval_{evaluation.pk}_{timestamp}.pdf'
    filepath  = os.path.join(pdf_dir, filename)

    # ── Document ─────────────────────────────────────────────────────────────
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleCustom',
        parent=styles['Title'],
        fontSize=18, fontName='Helvetica-Bold',
        textColor=INDIGO, alignment=TA_CENTER, spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        'SubtitleCustom',
        parent=styles['Normal'],
        fontSize=10, textColor=TEXT_MUTED, alignment=TA_CENTER, spaceAfter=14,
    )
    label_style = ParagraphStyle(
        'LabelCustom',
        parent=styles['Normal'],
        fontSize=9, fontName='Helvetica-Bold',
        textColor=TEXT_MUTED, spaceAfter=2,
    )
    value_style = ParagraphStyle(
        'ValueCustom',
        parent=styles['Normal'],
        fontSize=11, fontName='Helvetica',
        textColor=TEXT_MAIN, spaceAfter=10,
    )
    q_style = ParagraphStyle(
        'QuestionCustom',
        parent=styles['Normal'],
        fontSize=10, fontName='Helvetica-Bold',
        textColor=TEXT_MAIN, spaceAfter=2,
    )
    answer_style = ParagraphStyle(
        'AnswerCustom',
        parent=styles['Normal'],
        fontSize=10, fontName='Helvetica',
        textColor=TEXT_MUTED, spaceAfter=8, leftIndent=10,
    )

    story = []

    # ── En-tête ───────────────────────────────────────────────────────────────
    story.append(Paragraph("Rapport d'Évaluation", title_style))
    story.append(Paragraph(
        f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
        subtitle_style
    ))
    story.append(HRFlowable(width='100%', thickness=2, color=INDIGO, spaceAfter=16))

    # ── Infos générales ───────────────────────────────────────────────────────
    student_name = evaluation.student.get_full_name() or evaluation.student.username
    teacher_name = evaluation.teacher.get_full_name() or evaluation.teacher.username
    course_name  = evaluation.course.name
    dept_name    = evaluation.course.department.name
    level_name   = evaluation.course.level.name

    info_data = [
        ['Personne évaluée',  teacher_name],
        ['Département',        dept_name],
        ['Matière',            course_name],
        ['Niveau',             level_name],
        ['Type de cours',      'Général' if evaluation.course.is_general else 'Spécialisé'],
        ['Soumis le',          evaluation.updated_at.strftime('%d/%m/%Y à %H:%M')],
    ]

    info_table = Table(info_data, colWidths=[4.5*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('FONTNAME',     (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME',     (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE',     (0, 0), (-1, -1), 10),
        ('TEXTCOLOR',    (0, 0), (0, -1), TEXT_MUTED),
        ('TEXTCOLOR',    (1, 0), (1, -1), TEXT_MAIN),
        ('TOPPADDING',   (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID',         (0, 0), (-1, -1), 0.5, SLATE_BORDER),
        ('ROUNDEDCORNERS', [4]),
    ]))

    story.append(info_table)
    story.append(Spacer(1, 0.6*cm))

    # ── Score global ──────────────────────────────────────────────────────────
    answers       = list(evaluation.answers.select_related('question').all())
    scored_answers= [a for a in answers if a.question.type == 'scored' and a.score is not None]

    if scored_answers:
        avg_5   = sum(a.score for a in scored_answers) / len(scored_answers)
        avg_100 = round(avg_5 / 5 * 100, 1)

        color_100 = GREEN if avg_100 >= 70 else (AMBER if avg_100 >= 50 else RED)

        score_data = [['Score global', f'{avg_100} / 100', f'{avg_5:.1f} / 5']]
        score_table = Table(score_data, colWidths=[6*cm, 5.5*cm, 5.5*cm])
        score_table.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (-1, -1), INDIGO),
            ('TEXTCOLOR',     (0, 0), (0, 0),  colors.white),
            ('TEXTCOLOR',     (1, 0), (1, 0),  colors.white),
            ('TEXTCOLOR',     (2, 0), (2, 0),  colors.white),
            ('FONTNAME',      (0, 0), (0, 0),  'Helvetica-Bold'),
            ('FONTNAME',      (1, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE',      (0, 0), (-1, -1), 11),
            ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING',    (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('ROUNDEDCORNERS', [6]),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 0.6*cm))

    # ── Questions & réponses ──────────────────────────────────────────────────
    story.append(HRFlowable(width='100%', thickness=1, color=SLATE_BORDER, spaceAfter=10))
    story.append(Paragraph("Détail des réponses", ParagraphStyle(
        'SectionTitle', parent=styles['Normal'],
        fontSize=12, fontName='Helvetica-Bold',
        textColor=INDIGO, spaceAfter=10,
    )))

    for idx, answer in enumerate(answers, start=1):
        q = answer.question

        # Question text
        story.append(Paragraph(f"{idx}. {q.text}", q_style))

        if q.type == 'scored':
            score = answer.score
            stars = _stars(score)
            score_txt = f'{score} / 5  {stars}' if score is not None else '—'
            story.append(Paragraph(score_txt, answer_style))
        else:
            text = answer.text_answer or '(pas de réponse)'
            story.append(Paragraph(text, answer_style))

    # ── Pied de page ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.8*cm))
    story.append(HRFlowable(width='100%', thickness=1, color=SLATE_BORDER, spaceAfter=8))
    story.append(Paragraph(
        'Évaluation anonyme — Plateforme d\'Évaluation',
        ParagraphStyle('Footer', parent=styles['Normal'],
                       fontSize=8, textColor=TEXT_MUTED, alignment=TA_CENTER)
    ))

    doc.build(story)
    return filepath