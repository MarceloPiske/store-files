from django.conf import settings
from django.db import models


# Create your models here.
class DiretoriosS3(models.Model):
    
    nome = models.CharField(max_length=150, null=False, blank=False)
    arquivo = models.FileField(upload_to='media/temp/')
    pasta = models.CharField(max_length=150, default='media/', null=False)
    def __str__(self) -> str:
        return self.nome