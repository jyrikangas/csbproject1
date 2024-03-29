from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Note(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    secret = models.BooleanField(default=False)
