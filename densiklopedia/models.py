import uuid
from django.db import models
from django.conf import settings

class ArticleEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    judul = models.CharField(max_length=255)
    gambar = models.URLField(max_length=200)
    subjudul = models.CharField(max_length=500)
    konten = models.TextField()
    waktu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul

    def can_edit_delete(self, user):
        return self.user == user or user.is_superuser