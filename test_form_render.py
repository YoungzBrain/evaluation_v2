#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import Client
from accounts.models import User
from courses.models import Course

# Get a student, teacher, and course
student = User.objects.filter(role='student').first()
teacher = User.objects.filter(role='teacher').first()
course = Course.objects.filter(is_active=True).first()

if student and teacher and course:
    c = Client()
    c.force_login(student)
    r = c.get(f'/evaluate/teacher/{teacher.pk}/course/{course.pk}/')
    print('Status:', r.status_code)
    html = r.content.decode('utf-8')
    
    # Check for questions
    if 'question-block' in html:
        print('\n✓ Question blocks found in HTML')
        # Count them
        count = html.count('question-block')
        print(f'  Count: {count}')
    else:
        print('\n✗ No question blocks found')
    
    # Check for error messages
    if 'Aucune question' in html:
        print('✗ Error: "Aucune question"')
    elif 'Accès réservé' in html:
        print('✗ Error: Access denied')
    elif 'n\'avez pas accès' in html:
        print('✗ Error: No access to course')
    else:
        print('✓ No access errors')
    
    # Print relevant section
    if 'formulaire' in html.lower():
        idx = html.lower().find('formulaire')
        print('\n--- HTML around "formulaire" ---')
        print(html[max(0, idx-100):idx+300])
else:
    print(f'Missing: student={bool(student)}, teacher={bool(teacher)}, course={bool(course)}')
