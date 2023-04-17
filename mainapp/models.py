from django.db import models

# Create your models here.

class Usuario(models.Model):  # Modelo creado para ejecutar migraciones
    # Definir los datos de la clase (campos de la tabla)
    # Si no se especifica lo contrario, todos los campos seran requeridos por defecto, es decir NOT NULL
    first_name = models.CharField(max_length=150, verbose_name="Titulo")
    last_name = models.CharField(max_length=150, verbose_name="Descripcion")
    username = models.CharField(max_length=150, unique=True, verbose_name="Creado el")
    password = models.CharField(max_length=128, verbose_name="Entregado el")

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.username + ' ' + self.first_name + ' ' + self.last_name
