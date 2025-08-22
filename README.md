# FileOrganizer
Hice este organizador para acomodar toda mi carpeta de descargar, disfrutenlo

# Funcionalidades del Script:
## ✅ Organización automática:
Se guarda todo en las carpetas default de windows

Imágenes (.png, .webp, .jpg, .gif, .jpeg) → Carpeta "Imágenes"
Videos (.mp4, .mov) → Carpeta "Videos"
Música (.mp3, .opus) → Carpeta "Música"
Otros archivos permanecen en Descargas

# Features
* Log detallado - se crea un archivo .log con todas las operaciones realizadas
* Manejo de errores - si algo sale mal, el programa continúa con otros archivos
* Detección de archivos duplicados - si ya existe un archivo con el mismo nombre, se renombra automáticamente
* Solo mueve archivos - ignora las carpetas por seguridad
* Verificación de rutas - comprueba que las carpetas existan antes de mover archivos
* Windows multiidioma - funciona tanto con carpetas en inglés como en español
* Rutas automáticas - detecta automáticamente las carpetas de usuario

# Cómo usar el script:
1. Guarda el código como file_organizer.py
2. Ejecuta con doble clic o desde terminal: python organizador_descargas.py

# Para crear un ejecutable (.exe):
## usa: 
```
pip install pyinstaller
pyinstaller --onefile file_organizer.py
```
###Dentro de "dist/" hay un ejecutable ;)

