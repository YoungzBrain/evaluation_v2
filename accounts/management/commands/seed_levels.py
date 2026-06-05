from django.core.management.base import BaseCommand
from accounts.models import Level


class Command(BaseCommand):
    help = 'Seeds the database with levels Annee 1 to Annee 5'

    def handle(self, *args, **kwargs):
        levels = [
            {'name': 'Annee 1', 'order': 1},
            {'name': 'Annee 2', 'order': 2},
            {'name': 'Annee 3', 'order': 3},
            {'name': 'Annee 4', 'order': 4},
            {'name': 'Annee 5', 'order': 5},
        ]

        for level in levels:
            obj, created = Level.objects.get_or_create(
                name=level['name'],
                defaults={'order': level['order']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {obj.name}"))
            else:
                self.stdout.write(f"Already exists: {obj.name}")

        self.stdout.write(self.style.SUCCESS('Levels seeded successfully.'))