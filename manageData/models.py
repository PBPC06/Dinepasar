from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)  # Custom field for admin role