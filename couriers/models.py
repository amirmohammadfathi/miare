from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid


class Courier(AbstractBaseUser):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = None
    last_login = None

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

# Create your models here.
    def __str__(self):
        return str(self.id)

