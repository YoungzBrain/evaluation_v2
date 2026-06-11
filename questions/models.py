from django.db import models
from django.conf import settings


class PDFUpload(models.Model):
    file = models.FileField(upload_to='questions_pdfs/')
    original_filename = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.original_filename


class Question(models.Model):
    TYPE_CHOICES = [
        ('scored', 'Scored (1-5)'),
        ('open',   'Open text'),
    ]

    text      = models.TextField()
    type      = models.CharField(max_length=10, choices=TYPE_CHOICES, default='scored')
    is_active = models.BooleanField(default=True)
    source_pdf = models.ForeignKey(PDFUpload, null=True, blank=True, on_delete=models.SET_NULL, related_name='questions')
    pdf_page = models.PositiveIntegerField(null=True, blank=True)
    position = models.PositiveIntegerField(null=True, blank=True, help_text='Order within the source PDF')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.text[:80]