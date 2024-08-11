from django.db import models

# Create your models here.

class Usuario(models.Model):
    usuario = models.CharField(max_length=100)
    clave = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    rol = models.BigIntegerField()
    estado = models.BooleanField(default=True)