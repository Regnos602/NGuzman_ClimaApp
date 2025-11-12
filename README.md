# ClimaApp – Aplicación Web en Django  
*Autor:* Ignacio Guzmán  
*Carrera:* Técnico en Programación, Último año – Universidad Tecnológica Nacional (Argentina)  
*Actualmente en:* FASE (Soporte Técnico y Sistemas)  

---

## 🧭 Visión general  
ClimaApp es una aplicación web desarrollada con el framework Django que reúne dos funcionalidades centrales:  
1. Consulta del clima mediante la API Open‑Meteo API, ofreciendo datos meteorológicos actualizados.  
2. Formulario de contacto con almacenamiento en base de datos y envío de emails desde el panel de administración que Django ya proporciona.  

El objetivo es combinar una herramienta dinámica (el clima) con una funcionalidad práctica de contacto/gestión, para mostrar tanto la integración de APIs externas como el manejo interno de datos y correos.

---

## 🚀 Funcionalidades  
- Visualización de clima para una ubicación dada (latitud/longitud), utilizando Open-Meteo.  
- Formulario de contacto para visitantes: captura de nombre, email, mensaje, y registro de la entrada en la base de datos.  
- Envío automático de correo desde el administrador de Django al recibir un nuevo mensaje de contacto.  
- Backend listo para gestión (Django Admin) + frontend sencillo e intuitivo.  
- Código organizado, limpio y modular para facilitar mantenimiento o ampliación.

---

## 🧱 Tecnologías utilizadas  
- *Lenguaje:* Python 3.x  
- *Framework:* Django  
- *Base de datos:* SQLite (por defecto, para desarrollo)  
- *API de clima:* Open-Meteo API  
- *Frontend:* HTML5, CSS3, (posiblemente templating de Django)  
- *Correo:* Sistema de email nativo de Django configurado para envío desde el administrador.

---

## 🔧 Instalación y puesta en marcha  
1. Clonar el repositorio:  
   ```bash
   git clone https://github.com/Regnos602/NGuzman_ClimaApp.git
   cd NGuzman_ClimaApp
