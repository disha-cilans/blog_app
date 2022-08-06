from django.db import models
from django.contrib.auth.models import AbstractUser

class Blog(models.Model):
    title=models.CharField(max_length=50,null=False)
    content=models.TextField()
    author=models.CharField(max_length=50)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    