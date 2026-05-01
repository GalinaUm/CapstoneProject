from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Создает суперпользователя с предустановленными данными'

    def handle(self, *args, **options):
        email = 'admin@sky.pro'

        if not User.objects.filter(email=email).exists():
            user = User.objects.create_superuser(
                email=email,
                password='0987654321admin',
                first_name='Admin',
                last_name='SkyPro',
            )

            user.role = User.ADMIN
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f'Суперпользователь {email} успешно создан')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Пользователь {email} уже существует')
            )
