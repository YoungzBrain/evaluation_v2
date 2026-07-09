#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from evaluations.models import Evaluation, Answer

for e in Evaluation.objects.filter(status='submitted'):
    print(f'\nEval {e.pk}: {e.student.username} → {e.teacher.username} for {e.course}')
    answers = e.answers.all()
    scored = answers.filter(score__isnull=False).count()
    text = answers.filter(text_answer__isnull=False).exclude(text_answer='').count()
    print(f'  Answers: {scored} scored, {text} text, total: {answers.count()}')
    
    # Show scored answers
    for a in answers.filter(score__isnull=False):
        print(f'    Q{a.question.pk}: score={a.score}')
