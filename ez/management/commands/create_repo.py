from django.core.management.base import BaseCommand, CommandError
from ez.models import Repository
from django.contrib.auth.models import User
from django.conf import settings
import random
import string
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    TAB = '  '
    DOUBLETAB = '    '

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
            msg = bcolors.FAIL + 'Error:' + bcolors.ENDC
            msg += ' command needs a ' + bcolors.BOLD + 'password ' + bcolors.ENDC + 'entry.'
            msg += 'Try --help.'
            print( msg )
            return ''
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
                print( bcolors.FAIL + 'Error:' + bcolors.ENDC + ' name already taken.' )
                return ''
        # Create the user bound to the repository
        user = User.objects.create_user(name, '', password)
        user.save()
        # Create the repository
        repository = Repository(owner=user)
        repository.save()
        # Finally, create the target folder
        os.makedirs(settings.UPLOAD_DIR+name)
        msg = bcolors.OKGREEN + 'Success:' +bcolors.ENDC
        msg += ' repository ' + bcolors.BOLD + name + bcolors.ENDC + ' created !'
        print( msg )
        return ''
