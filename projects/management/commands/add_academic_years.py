from django.core.management.base import BaseCommand
from projects.models import AcademicYear
from datetime import datetime

class Command(BaseCommand):
    help = 'Add academic years to the database from 2002 to current year'

    def handle(self, *args, **options):
        current_year = datetime.now().year
        start_year = 2002
        
        created_count = 0
        
        for year in range(start_year, current_year + 1):
            year_str = f"{year}-{year + 1}"
            academic_year, created = AcademicYear.objects.get_or_create(year=year_str)
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {year_str}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Already exists: {year_str}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Total created: {created_count} academic years')
        )
