from django.db import models
from django.contrib.auth.models import User

class Repository(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Files(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
