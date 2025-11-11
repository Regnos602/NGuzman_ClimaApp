from django.db import models

class MensajeContacto(models.Model): #Clase para que el mensaje mandado en el formulario quede registrado
    nombre = models.CharField(max_length=25) #validacion de no mas de 25 caracteres
    email = models.EmailField() 
    mensaje = models.CharField() 
    creado_en = models.DateTimeField(auto_now_add=True) #Fecha de creacion

    def __str__(self):
        return f"{self.nombre} <{self.email}> - {self.creado_en:%Y-%m-%d %H:%M}"

