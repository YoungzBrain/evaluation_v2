from django.core.management.base import BaseCommand
from pathlib import Path
import csv

class Command(BaseCommand):
    help = 'Backup all questions to backup_questions.csv and delete them from DB'

    def handle(self, *args, **options):
        try:
            from questions.models import Question
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f'Failed to import Question model: {exc}'))
            return

        qs = Question.objects.all()
        total = qs.count()
        if total == 0:
            self.stdout.write('No questions found in DB.')
            return

        # Backup
        backup_path = Path.cwd() / 'backup_questions.csv'
        with backup_path.open('w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['text', 'type', 'is_active'])
            for q in qs:
                writer.writerow([q.text, q.type, '1' if q.is_active else '0'])

        # Delete
        deleted, _ = qs.delete()

        self.stdout.write(self.style.SUCCESS(f'Backed up {total} questions to {backup_path}'))
        self.stdout.write(self.style.SUCCESS(f'Deleted {total} questions (deleted rows reported: {deleted})'))
