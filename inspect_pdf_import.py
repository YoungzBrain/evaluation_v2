import django
import os
import sys

# Ensure project root in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from questions.models import PDFUpload, Question

print('PDFUpload count:', PDFUpload.objects.count())
for pdf in PDFUpload.objects.all():
    print('PDF', pdf.pk, pdf.original_filename, 'created', pdf.created_at)
    qs = Question.objects.filter(source_pdf=pdf)
    print('  sourced questions', qs.count(), 'active', qs.filter(is_active=True).count())
    for q in qs:
        print('   ', q.pk, q.type, q.is_active, q.pdf_page, q.position, repr(q.text[:60]))
