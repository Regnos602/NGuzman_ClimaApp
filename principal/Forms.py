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

    def clean_email(self): #Funcion de validación extra personalizada para emails
        email = self.cleaned_data["email"]
        if not email.endswith(".com"):
            raise forms.ValidationError("Solo se aceptan correos que terminen en .com")
        return email