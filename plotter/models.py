from django.db import models

# Create your models here.

class Directory(models.Model):
    path = models.CharField(max_length=255)

class Folder(models.Model):
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='pictures/', blank=True, null=True)
