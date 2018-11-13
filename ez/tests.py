from django.test import TestCase
from .models import Repository
from django.contrib.auth.models import User

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
