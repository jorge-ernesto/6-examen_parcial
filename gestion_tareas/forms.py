from django import forms
from django.core import validators

class FormTarea(forms.Form):
    # Definir los datos de la clase (inputs del formulario)
    # Si no se especifica lo contrario, todos los inputs seran required=TRUE por defecto
    title = forms.CharField(
        label = "Titulo",
        max_length = 20,
        required = True,
        validators = [
            validators.MinLengthValidator(4, 'El titulo es demasiado corto'),
            validators.RegexValidator('^[A-Za-z0-9ñ ]*$', 'El titulo esta mal formado', 'invalid_title')
        ]
    )

    description = forms.CharField(
        label = "Descripción",
        required = True,
        validators = [
            validators.MaxLengthValidator(50, 'Te has pasado, has puesto mucho texto')
        ]
    )

    delivery_at = forms.DateTimeField(
        label = "Entregado el",
        required = True
    )
