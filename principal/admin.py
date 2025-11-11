from django.contrib import admin
from .models import MensajeContacto

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "creado_en")       # columnas en la lista
    search_fields = ("nombre", "email", "mensaje")        # caja de busqueda
    list_filter = ("creado_en",)                          # filtro lateral por fecha
    date_hierarchy = "creado_en"                          # navegacion por fecha arriba
    ordering = ("-creado_en",)                            # ultimos primero
    readonly_fields = ("creado_en",)                      # no editable