from django.db import models
from django.contrib.auth.models import User

class Moto(models.Model):# modelo de la moto que se importan a la base de datos
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    placa = models.CharField(max_length=100, unique=True)
    observaciones = models.TextField(blank=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='motos', null=True, blank=True)



    def __str__(self):
        return f"{self.year} {self.marca} {self.modelo}" # Representacion legible de la moto
    