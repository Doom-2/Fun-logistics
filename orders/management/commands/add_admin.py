import environ
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

env = environ.Env()


class Command(BaseCommand):
    help = "Creates the first superuser in table 'User' if one does not exist. Credentials are taken from .env"

    def handle(self, *args, **kwargs) -> None:
        username = env('DJANGO_SUPERUSER_NAME')
        password = env('DJANGO_SUPERUSER_PASSWORD')

        user = get_user_model().objects.filter(username=username).first()
        if not user:
            get_user_model().objects.create_superuser(username=username, password=password, email='')
            self.stdout.write(
                self.style.SUCCESS(f'Superuser {username} created successfully.'))
            return
        else:
            self.stdout.write(
                self.style.ERROR(f'Superuser {username} already exists.'
                                 f'\nCreate another one via \'python3 manage.py createsuperuser\' command'))
