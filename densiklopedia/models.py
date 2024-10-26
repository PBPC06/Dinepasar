import uuid
from django.db import models
from django.contrib.auth.models import User

class ArticleEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    judul = models.CharField(max_length=255)
    gambar = models.URLField(max_length=200)
    subjudul = models.CharField(max_length=500)
    konten = models.TextField()
    waktu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul

    def can_edit_delete(self, user):
        # To check if the article can be edited or deleted by the current user
        return self.user == user