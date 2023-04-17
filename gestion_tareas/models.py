from django.db import models
from mainapp.models import Usuario

# Create your models here.

class Tarea(models.Model):  # Modelo creado para ejecutar migraciones
    # Definir los datos de la clase (campos de la tabla)
    # Si no se especifica lo contrario, todos los campos seran requeridos por defecto, es decir NOT NULL
    title = models.CharField(max_length=50, verbose_name="Titulo")
    description = models.TextField(verbose_name="Descripcion")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    delivery_at = models.DateTimeField(verbose_name="Entregado el")
    usuario = models.ForeignKey(Usuario, editable=False, verbose_name="Usuario", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Tarea"  # Manipular nombre en el panel
        verbose_name_plural = "Tareas"  # Manipular nombre en el panel

    def __str__(self):
        return self.title
