from django import forms
from .models import MensajeContacto 

class ContactoForm(forms.ModelForm): #Clase de formularios para contacto
    class Meta:
        model = MensajeContacto
        fields = ["nombre", "email", "mensaje"] #Los distintos formularios en el mismo

        labels = {
            "nombre": "Nombre",
            "email": "Correo electrónico",
            "mensaje": "Mensaje",
        }

        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre completo",
            }),
            
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "usuario@ejemplo.com",
            }),
            "mensaje": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Escribí tu problema",
            }),
        }

        error_messages = { #Validaciones basicas
            "nombre": {
                "required": "Por favor, escribí un nombre válido.",
            },
            "email": {
                "required": "Ingresá un mail válido.",
                "invalid": "Ingresá un correo electrónico válido (ejemplo@dominio.com).",
            },
            "mensaje": {
                "required": "El mensaje no puede estar vacío.",
            },
        }



class ClimaForm(forms.Form): #Clase de formularios para poder hacer busqueda del tiempo en la ubicacion que el usuario otorgue
    ubicacion = forms.CharField(
        label="Ciudad o Localidad",
        max_length=80,
        widget=forms.TextInput(attrs={ 
            "class": "form-control",
            "placeholder": "Ej: Buenos Aires, AR",
            "autocomplete": "off",
        }),
        error_messages={"required": "Escribí una ciudad."}
    )
    lat = forms.FloatField(required=False, widget=forms.HiddenInput()) #Ocultar los campos para que al usuario no le aparezcan las opciones hasta que escriba algo en el texto
    lon = forms.FloatField(required=False, widget=forms.HiddenInput())