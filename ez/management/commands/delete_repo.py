from django.core.management.base import BaseCommand, CommandError
from ez.models import Repository
from django.contrib.auth.models import User
from django.conf import settings
import random
import string
import shutil

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
    help = 'Deletes a repository.'

    def add_arguments(self, parser):
        parser.add_argument('--name',
            dest='name',
            help='Name of the repository.',)

        parser.add_argument('--id',
            dest='id',
            type=int,
            help='Id of the repository.',)

    def handle(self, *args, **options):
        # Retrieve password. If there's none, exit.
        name = options['name']
        user = None
        if name is None:
            id = options['id']
            if id is None:
                msg = bcolors.FAIL + 'Error:' + bcolors.ENDC
                msg += ' command needs a ' + bcolors.BOLD + 'name ' + bcolors.ENDC
                msg += 'or an ' + bcolors.BOLD + 'id. ' +bcolors.ENDC
                msg += 'Try --help.'
                print( msg )
                return ''
            else:
                try:
                    name = Repository.objects.get(pk=id).owner.username
                except Repository.DoesNotExist:
                    print( bcolors.FAIL + 'Error:' + bcolors.ENDC + ' Repository does not exist.' )
                    return ''
        try:
            user = User.objects.get(username=name)
        except User.DoesNotExist:
            print( bcolors.FAIL + 'Error:' + bcolors.ENDC + ' Repository does not exist.' )
            return ''
        user.delete()
        shutil.rmtree(settings.UPLOAD_DIR+name)
        msg = bcolors.OKGREEN + 'Success:' +bcolors.ENDC
        msg += ' repository ' + bcolors.BOLD + name + bcolors.ENDC + ' deleted !'
        print( msg )
        return ''
