from django.test import TestCase
from .models import Repository
from django.contrib.auth.models import User
from django.core.management import call_command
from io import StringIO

class RepositoryModelTests(TestCase):

    def test_create_repository(self):
        """
        Check the creation of a repository.
        """
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        repository = Repository(owner=user)
        repository.save()
        self.assertNotEqual(repository.id, 0)

class RepositoryCommandTests(TestCase):

    def test_create_repository(self):
        """
        Check the creation of a repository.
        """
        out = StringIO()
        # Create a first repo.
        call_command('create_repo', password='abc', name='john', stdout=out)
        user = User.objects.filter(username='john').first()
        self.assertIsNotNone(user)
        repo = Repository.objects.filter(owner=user).first()
        self.assertIsNotNone(repo)
        # flush out
        out = StringIO()
        # Create the same repo
        call_command('create_repo', password='abc', name='john', stdout=out)
        users = User.objects.filter(username='john').count()
        self.assertEqual(users, 1)
        repos = Repository.objects.filter(owner=user).count()
        self.assertEqual(repos, 1)
        # flush out
        out = StringIO()
        # Create a new repo
        call_command('create_repo', password='abc', name='john2', stdout=out)
        users = User.objects.filter(username='john2').count()
        self.assertEqual(users, 1)
        repos = Repository.objects.count()
        self.assertEqual(repos, 2)
        # flush out
        out = StringIO()
        # Create a new random repo
        call_command('create_repo', password='abc', stdout=out)
        users = User.objects.count()
        self.assertEqual(users, 3)
        repos = Repository.objects.count()
        self.assertEqual(repos, 3)
        # flush out
        out = StringIO()
        # Create a repo without password
        call_command('create_repo', stdout=out)
        users = User.objects.count()
        self.assertEqual(users, 3)
        repos = Repository.objects.count()
        self.assertEqual(repos, 3)
        # flush out
        out = StringIO()
        # Create a repo without password
        call_command('create_repo', name='john3', stdout=out)
        users = User.objects.count()
        self.assertEqual(users, 3)
        repos = Repository.objects.count()
        self.assertEqual(repos, 3)
