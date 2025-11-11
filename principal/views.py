from django.shortcuts import render,redirect
from .Forms import ContactoForm
from django.contrib import messages

def inicio(request): #Inicio de la pagina
    contexto = {"nombre": "Campeon"}
    return render(request, "principal/index.html", contexto)

def acerca(request): #Acerca de la pagina
    return render(request, "principal/acerca.html")

def contacto(request): #Contacto de la pagina
    if request.method == "POST":
        form = ContactoForm(request.POST) #Crea el formulario con los datos ingresados
        if form.is_valid(): 
            form.save()  #Guarda lo ingresado en una BD
            messages.success(request, "¡Gracias! Tu mensaje fue enviado.")
            return redirect("contacto")  #evita reenvios masivos con F5
    else:
        form = ContactoForm()

    return render(request, "principal/contacto.html", {"form": form})