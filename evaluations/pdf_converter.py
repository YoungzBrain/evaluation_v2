import csv
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from django.conf import settings


def csv_to_pdf(csv_filepath, output_filename=None):
    """
    Convert a CSV file to a PDF with a table layout.

    Args:
        csv_filepath: Path to the CSV file
        output_filename: Optional output filename (defaults to timestamp-based name)

    Returns:
        Path to the generated PDF file
    """

    # Ensure media directory exists
    media_root = getattr(settings, 'MEDIA_ROOT', os.path.join(settings.BASE_DIR, 'media'))
    pdfs_dir = os.path.join(media_root, 'questions_pdfs')
    os.makedirs(pdfs_dir, exist_ok=True)

    # Generate output filename if not provided
    if not output_filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f'csv_import_{timestamp}.pdf'

    output_path = os.path.join(pdfs_dir, output_filename)

    # Parse CSV
    rows = []
    try:
        with open(csv_filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except Exception as exc:
        raise ValueError(f"Failed to read CSV file: {exc}")

    if not rows:
        raise ValueError("CSV file is empty")

    # Create PDF
    doc = SimpleDocTemplate(output_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=12,
    )

    question_style = ParagraphStyle(
        'Question',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=colors.HexColor('#0f172a'),
        leftIndent=10,
        rightIndent=10,
        spaceAfter=8,
    )

    # Add title
    elements.append(Paragraph("Questionnaire d'Évaluation", title_style))
    elements.append(Spacer(1, 0.2*inch))

    # Build table data
    table_data = [['#', 'Question']]

    for idx, row in enumerate(rows, 1):
        text = row.get('text', '').strip()
        if text:
            try:
                question_para = Paragraph(text, question_style)
                table_data.append([str(idx), question_para])
            except Exception:
                # Fallback if paragraph rendering fails
                table_data.append([str(idx), text[:200]])

    if len(table_data) <= 1:
        raise ValueError("No valid questions found in CSV")

    # Create table
    table = Table(table_data, colWidths=[0.4*inch, 6*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#334155')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8fafc'), colors.HexColor('#f1f5f9')]),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
    ]))

    elements.append(table)

    # Build PDF
    try:
        doc.build(elements)
    except Exception as exc:
        raise ValueError(f"Failed to generate PDF: {exc}")

    return output_path
