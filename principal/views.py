from django.shortcuts import render,redirect
from .Forms import ContactoForm,ClimaForm
from django.contrib import messages
import requests



def inicio(request):
    contexto = {"nombre": "None"}    
    datos, errores = None, None #Inicializaciones

    if request.method == "GET" and (request.GET.get("ubicacion") or request.GET.get("lat")): #Busqueda de la ubicacion ingresada por el usuario
        form_clima = ClimaForm(request.GET)
        if form_clima.is_valid(): #Validaciones de formulario
            lat = form_clima.cleaned_data.get("lat")
            lon = form_clima.cleaned_data.get("lon")
            q   = form_clima.cleaned_data["ubicacion"].strip()

            if lat is not None and lon is not None: #coordenadas ya traidas (usuario selecciono una opcion)
                lugar = q 
            else: #coordenadas buscadas (usuario no selecciono una opcion)
                geo = requests.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={"name": q, "count": 1, "language": "es"},
                    timeout=7
                ).json()
                if not geo.get("results"): #no resultados a la opcion dada (mensaje de error)
                    errores = f"No encontré: {q}. Probá con país/código (ej: Córdoba, AR)."
                    contexto.update({"form_clima": form_clima, "clima": None, "clima_error": errores})
                r0 = geo["results"][0] #si hubo resultados, toma las coordenadas
                lat, lon = r0["latitude"], r0["longitude"]
                lugar = f'{r0["name"]}, {r0.get("country_code","")}'

            meteo = requests.get( #llamada a la api del pronostico  
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat, "longitude": lon,
                    "current": "temperature_2m,weather_code",
                    "daily": "temperature_2m_max,temperature_2m_min,weather_code",
                    "timezone": "auto", "forecast_days": 7
                },
                timeout=7
            ).json()

            current = meteo.get("current", {}) #tiempo actual
            daily = meteo.get("daily", {}) #tiempo diario
            pronostico = []
            for i, fecha in enumerate(daily.get("time", [])):
                code = daily["weather_code"][i]
                pronostico.append({
                    "fecha": fecha,
                    "tmax": daily["temperature_2m_max"][i],
                    "tmin": daily["temperature_2m_min"][i],
                    "cond": WMO.get(code, f"Código {code}")
                })

            datos = {
                "lugar": lugar,
                "temp_actual": current.get("temperature_2m"),
                "cond_actual": WMO.get(current.get("weather_code", -1), "—"),
                "pronostico": pronostico
            }
    else:
        form_clima = ClimaForm()

    contexto.update({"form_clima": form_clima, "clima": datos, "clima_error": errores})
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


WMO = { #Libreria de distintas opciones de texto dependiendo el numero que la API nos de
    0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado", 3: "Nublado",
    45: "Niebla", 48: "Niebla con escarcha",
    51: "Llovizna débil", 53: "Llovizna", 55: "Llovizna intensa",
    61: "Lluvia débil", 63: "Lluvia", 65: "Lluvia intensa",
    71: "Nieve débil", 73: "Nieve", 75: "Nieve intensa",
    80: "Chaparrón débil", 81: "Chaparrón", 82: "Chaparrón fuerte",
    95: "Tormenta", 96: "Tormenta con granizo", 99: "Tormenta fuerte con granizo"
}
