from django.db import models


class Question(models.Model):
    TYPE_CHOICES = [
        ('scored', 'Scored (1-5)'),
        ('open',   'Open text'),
    ]

    text      = models.TextField()
    type      = models.CharField(max_length=10, choices=TYPE_CHOICES, default='scored')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.text[:80]