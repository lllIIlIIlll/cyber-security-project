from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    content = models.CharField(max_length=140)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)