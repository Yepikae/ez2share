from django.core.management.base import BaseCommand, CommandError
from ez.models import Repository
from django.contrib.auth.models import User
from django.conf import settings
import random
import string
import shutil

class Command(BaseCommand):
    help = 'Deletes a repository.'

    def add_arguments(self, parser):
        parser.add_argument('--name',
            dest='name',
            help='Name of the repository.',)

    def handle(self, *args, **options):
        # Retrieve password. If there's none, exit.
        name = options['name']
        if name is None:
            return "Name required"
        # Retrieve name. Id there's none, create a unique random one.
        name = options['name']
        user = None
        try:
            user = User.objects.get(username=name)
        except User.DoesNotExist:
            return "Repository does not exist."
        user.delete()
        shutil.rmtree(settings.UPLOAD_DIR+name)
        return "Ok"
