from django.core.management.base import BaseCommand, CommandError
from ez.models import Repository
from django.contrib.auth.models import User
import random
import string

class Command(BaseCommand):
    help = 'Creates a new repository.'
    name_length = 16

    def add_arguments(self, parser):
        parser.add_argument('--name',
            dest='name',
            help='Name of the repository.',)

        parser.add_argument('--password',
            dest='password',
            help='Required! Password of the repository.',)

    def handle(self, *args, **options):
        # Retrieve password. If there's none, exit.
        password = options['password']
        if password is None:
            return "Password required"
        # Retrieve name. Id there's none, create a unique random one.
        name = options['name']
        if name is None:
            # Create a random name.
            def _create_name(N):
                upper = string.ascii_uppercase
                lower = string.ascii_lowercase
                return ''.join(random.SystemRandom().choice(upper + lower) for _ in range(N))
            # Loop while random name doesn't exist yet.
            name = _create_name(self.name_length)
            while(User.objects.filter(username=name).first() is not None):
                name = _create_name(self.name_length)
        else:
            if User.objects.filter(username=name).first() is not None:
                return "Name already taken"
        # Create the user bound to the repository
        user = User.objects.create_user(name, '', password)
        user.save()
        # Finally create the repository
        repository = Repository(owner=user)
        repository.save()
        return "Ok"
