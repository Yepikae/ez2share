from django.core.management.base import BaseCommand, CommandError
from ez.models import Repository, Files
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
    help = 'List all the repositories.'

    # Uncomment to add some arguments
    # def add_arguments(self, parser):
    #     parser.add_argument('--name',
    #         dest='name',
    #         help='Name of the repository.',)

    def handle(self, *args, **options):
        repositories = Repository.objects.all()
        for repo in repositories:
            print( bcolors.OKBLUE + repo.owner.username + bcolors.ENDC )
            print( '├─ id n° ' + str(repo.id))
            print( '├─ created the ' + str(repo.created_at.date()))
            print( '└─ files')
            files = Files.objects.filter(repository=repo)
            tree_symbol = '├─ '
            for index, file in enumerate(files):
                if index == len(files) - 1:
                    tree_symbol = '└─ '
                print(bcolors.DOUBLETAB + tree_symbol + file.filename)
        return '.'
