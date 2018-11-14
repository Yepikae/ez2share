from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os

class Repository(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return settings.UPLOAD_DIR+'{0}/{1}'.format(instance.repository.owner.username, filename)

class Files(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)

    @property
    def filename(self):
        return os.path.basename(self.file.name)
