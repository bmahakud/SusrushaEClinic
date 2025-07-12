from django.core.management.base import BaseCommand
from account.models import UserType

class Command(BaseCommand):
    help = 'Set up initial data for the e-clinic system'

    def handle(self, *args, **options):
        # Create UserType entries
        user_types = [
            'super_admin',
            'clinic_admin', 
            'doctor',
            'patient'
        ]
        
        for user_type_name in user_types:
            user_type, created = UserType.objects.get_or_create(name=user_type_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created UserType: {user_type_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'UserType already exists: {user_type_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Initial data setup completed successfully!')
        ) 