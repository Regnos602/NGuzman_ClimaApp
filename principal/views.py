from django.shortcuts import render,redirect
from .Forms import ContactoForm,ClimaForm
from django.contrib import messages
from datetime import datetime
import requests


def inicio(request):
    """Funcion de inicio en el cual se encuentran las distintas validaciones, busquedas y respuestas de la aplicacion de clima.

    Args:
        request (HttpRequest): Peticion http recibida desde el navegador. Puede contener datos GET enviados por el form del clima.

    Returns:
        HttpResponse: Pagina HTML renderizada que contiene formulario de busqueda, resultados del clima con sus validaciones.
    """

    # Contexto base
    contexto = {"nombre": "None"}
    datos = None
    errores = None

    if request.method == "GET" and (
        request.GET.get("ubicacion") or request.GET.get("lat")
    ):
        form_clima = ClimaForm(request.GET)

        if form_clima.is_valid():
            # Tomamos datos del formulario
            lat = form_clima.cleaned_data.get("lat")
            lon = form_clima.cleaned_data.get("lon")
            q = form_clima.cleaned_data.get("ubicacion").strip()

            # Si NO tenemos lat/lon (porque el usuario escribió a mano la ciudad),
            # usamos la API de geocoding de Open-Meteo para buscarlas
            if lat is None or lon is None:
                geo = requests.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={
                        "name": q,
                        "count": 1,
                        "language": "es",
                    },
                    timeout=7,
                ).json()

                if not geo.get("results"):
                    errores = f"No encontré: {q}. Probá con país/código (ej: Córdoba, AR)."
                    contexto.update({
                        "form_clima": form_clima,
                        "clima": None,
                        "clima_error": errores,
                    })
                    return render(request, "principal/index.html", contexto)

                r0 = geo["results"][0]
                lat = r0["latitude"]
                lon = r0["longitude"]
                lugar = f'{r0["name"]}, {r0.get("country_code","")}'
            else:
                # Si ya teníamos lat/lon desde la sugerencia
                lugar = q

            #Llamada a la API del pronóstico 
            meteo = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,weather_code",
                    "daily": "temperature_2m_max,temperature_2m_min,weather_code",
                    "timezone": "auto",
                    "forecast_days": 7,
                },
                timeout=7,
            ).json()

            current = meteo.get("current", {})
            daily = meteo.get("daily", {})

            tiempos = daily.get("time", [])
            codigos = daily.get("weather_code", [])
            tmaxs = daily.get("temperature_2m_max", [])
            tmins = daily.get("temperature_2m_min", [])

            pronostico = []
            for i, fecha in enumerate(tiempos):
                if i >= len(codigos) or i >= len(tmaxs) or i >= len(tmins):
                    continue

                code = codigos[i]
                tmax = tmaxs[i]
                tmin = tmins[i]

                try:
                    fecha_date = datetime.strptime(fecha, "%Y-%m-%d").date()
                    dia_semana = DIAS_SEMANA[fecha_date.weekday()]
                except Exception:
                    dia_semana = ""

                pronostico.append({
                    "fecha": fecha,
                    "dia": dia_semana,
                    "tmax": tmax,
                    "tmin": tmin,
                    "cond": WMO.get(code, f"Código {code}"),
                })

            # Diccionario que se manda al template
            datos = {
                "lugar": lugar,
                "temp_actual": current.get("temperature_2m"),
                "cond_actual": WMO.get(current.get("weather_code"), ""),
                "pronostico": pronostico,
            }

            contexto.update({
                "form_clima": form_clima,
                "clima": datos,
                "clima_error": errores,
            })
        else:
            # Formulario no válido, lo devolvemos con errores
            contexto.update({
                "form_clima": form_clima,
                "clima": None,
                "clima_error": "Revisá los datos del formulario.",
            })

    else:
        # Primera carga de la página o sin parámetros: formulario vacío
        form_clima = ClimaForm()
        contexto.update({
            "form_clima": form_clima,
            "clima": None,
            "clima_error": None,
        })
    return render(request, "principal/index.html", contexto)

def acerca(request):
    """Vista informativa de la pagina, renderiza la seccion de "Acerca".

    Args:
        request (HttpRequest): Peticion HTTP realizada por el usuario al ingresar a la pagina.

    Returns:
        HttpResponse: Pagina HTML con la descripcion informativa del proyecto ReClima.
    """
    return render(request, "principal/acerca.html")

def contacto(request):
    """Vista encargada de gestionar el formulario de contacto del sitio.

    Args:
        request (HttpRequest): peticion HTTP realizada por el usuario. Puede contener 
        informacion enviada mediante POST si el usuario completo el formulario.

    Returns:
        HttpResponse: Pagina ya renderizada con el formulario de contacto y las validaciones de respuestas.
    """
    if request.method == "POST":
        form = ContactoForm(request.POST) #Crea el formulario con los datos ingresados
        if form.is_valid(): 
            form.save()  #Guarda lo ingresado en una BD
            messages.success(request, "¡Gracias! Tu mensaje fue enviado.")
            return redirect("contacto")  #evita reenvios masivos con F5
    else:
        form = ContactoForm()

    return render(request, "principal/contacto.html", {"form": form})


WMO = { #Diccionario de distintas opciones de texto dependiendo el numero que la API nos de
    0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado", 3: "Nublado",
    45: "Niebla", 48: "Niebla con escarcha",
    51: "Llovizna débil", 53: "Llovizna", 55: "Llovizna intensa",
    61: "Lluvia débil", 63: "Lluvia", 65: "Lluvia intensa",
    71: "Nieve débil", 73: "Nieve", 75: "Nieve intensa",
    80: "Chaparrón débil", 81: "Chaparrón", 82: "Chaparrón fuerte",
    95: "Tormenta", 96: "Tormenta con granizo", 99: "Tormenta fuerte con granizo"
}

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]