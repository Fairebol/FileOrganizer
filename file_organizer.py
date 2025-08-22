#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Organizador Automático de Archivos de Descargas
Mueve archivos desde la carpeta Descargas a carpetas organizadas por tipo
"""

import os
import shutil
import pathlib
from pathlib import Path
import logging
from datetime import datetime

def configurar_logging():
    """Configura el sistema de logging para registrar las operaciones"""
    log_filename = f"organizador_archivos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def obtener_carpetas_predeterminadas():
    try:
        # Usar pathlib para obtener las carpetas del usuario
        carpeta_usuario = Path.home()
        
        carpetas = {
            'descargas': carpeta_usuario / "Downloads",
            'imagenes': carpeta_usuario / "Pictures", 
            'videos': carpeta_usuario / "Videos",
            'musica': carpeta_usuario / "Music"
        }
        
        carpeta_descargas_es = carpeta_usuario / "Descargas"
        if carpeta_descargas_es.exists():
            carpetas['descargas'] = carpeta_descargas_es
            
        carpeta_imagenes_es = carpeta_usuario / "Imágenes"
        if carpeta_imagenes_es.exists():
            carpetas['imagenes'] = carpeta_imagenes_es
            
        carpeta_videos_es = carpeta_usuario / "Vídeos"
        if carpeta_videos_es.exists():
            carpetas['videos'] = carpeta_videos_es
            
        carpeta_musica_es = carpeta_usuario / "Música"
        if carpeta_musica_es.exists():
            carpetas['musica'] = carpeta_musica_es
        
        return carpetas
        
    except Exception as e:
        raise Exception(f"Error al obtener carpetas predeterminadas: {e}")

def crear_carpetas_si_no_existen(carpetas):
    for nombre, ruta in carpetas.items():
        if nombre != 'descargas':  # No crear carpeta descargas
            try:
                ruta.mkdir(parents=True, exist_ok=True)
                print(f"✓ Carpeta verificada: {ruta}")
            except Exception as e:
                print(f"⚠ Error al crear/verificar carpeta {nombre}: {e}")

def definir_extensiones():
    """Define los tipos de archivos y sus extensiones correspondientes"""
    return {
        'imagenes': {'.png', '.webp', '.jpg', '.gif', '.jpeg'},
        'videos': {'.mp4', '.mov'},
        'musica': {'.mp3', '.opus'}
    }

def mover_archivo_con_seguridad(archivo_origen, carpeta_destino, logger):
    """Mueve un archivo de forma segura, manejando conflictos de nombres"""
    try:
        nombre_archivo = archivo_origen.name
        archivo_destino = carpeta_destino / nombre_archivo
        
        contador = 1
        nombre_base = archivo_origen.stem
        extension = archivo_origen.suffix
        
        while archivo_destino.exists():
            nuevo_nombre = f"{nombre_base}_{contador}{extension}"
            archivo_destino = carpeta_destino / nuevo_nombre
            contador += 1
        
        shutil.move(str(archivo_origen), str(archivo_destino))
        logger.info(f"Movido: {nombre_archivo} → {carpeta_destino.name}")
        print(f"✓ {nombre_archivo} → {carpeta_destino.name}")
        return True
        
    except Exception as e:
        logger.error(f"Error al mover {archivo_origen.name}: {e}")
        print(f"✗ Error al mover {archivo_origen.name}: {e}")
        return False

def organizar_archivos():
    """Función principal que organiza los archivos"""
    logger = configurar_logging()
    logger.info("=== INICIANDO ORGANIZACION DE ARCHIVOS ===")
    print("🗂️  Iniciando organización de archivos...")
    
    try:
        carpetas = obtener_carpetas_predeterminadas()
        carpeta_descargas = carpetas['descargas']
        
        if not carpeta_descargas.exists():
            raise Exception(f"La carpeta de descargas no existe: {carpeta_descargas}")
        
        print(f"📁 Carpeta de descargas: {carpeta_descargas}")
        
        crear_carpetas_si_no_existen(carpetas)
        
        extensiones_por_tipo = definir_extensiones()
        
        archivos_movidos = 0
        errores = 0
        archivos_ignorados = 0
        
        archivos = [f for f in carpeta_descargas.iterdir() if f.is_file()]
        
        if not archivos:
            print("ℹ️  No se encontraron archivos en la carpeta de descargas.")
            return
        
        print(f"🔍 Se encontraron {len(archivos)} archivos para procesar...")
        
        for archivo in archivos:
            extension = archivo.suffix.lower()
            
            tipo_encontrado = None
            carpeta_destino = None
            
            for tipo, extensiones_set in extensiones_por_tipo.items():
                if extension in extensiones_set:
                    tipo_encontrado = tipo
                    carpeta_destino = carpetas[tipo]
                    break
            
            if tipo_encontrado:
                if mover_archivo_con_seguridad(archivo, carpeta_destino, logger):
                    archivos_movidos += 1
                else:
                    errores += 1
            else:
                archivos_ignorados += 1
                logger.info(f"Ignorado (extensión no definida): {archivo.name}")
                print(f"- {archivo.name} (permanece en Descargas)")
        
        # Resumen final
        print("\n" + "="*50)
        print("📊 RESUMEN DE LA ORGANIZACIÓN:")
        print(f"✅ Archivos movidos: {archivos_movidos}")
        print(f"⚠️  Errores: {errores}")
        print(f"➡️  Archivos que permanecen en Descargas: {archivos_ignorados}")
        print("="*50)
        
        logger.info(f"=== ORGANIZACION COMPLETADA - Movidos: {archivos_movidos}, Errores: {errores}, Ignorados: {archivos_ignorados} ===")
        
    except Exception as e:
        error_msg = f"Error general en la organización: {e}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")

def mostrar_ayuda():
    """Muestra información sobre el programa"""
    print("""
🗂️  ORGANIZADOR DE ARCHIVOS DE DESCARGAS
==========================================

Este programa organiza automáticamente los archivos de tu carpeta Descargas:

📸 IMÁGENES → Carpeta Imágenes/Pictures
   • .png, .webp, .jpg, .gif, .jpeg

🎬 VIDEOS → Carpeta Videos
   • .mp4, .mov

🎵 MÚSICA → Carpeta Música/Music
   • .mp3, .opus

ℹ️  OTROS ARCHIVOS permanecen en Descargas

⚠️  RECOMENDACIONES:
• Haz una copia de seguridad antes de ejecutar
• El programa crea un log con todas las operaciones
• Si hay archivos con el mismo nombre, se renombran automáticamente
• Solo se procesan archivos, las carpetas se ignoran

¿Continuar? (s/n): """)

if __name__ == "__main__":
    print("🗂️  ORGANIZADOR DE ARCHIVOS DE DESCARGAS")
    print("="*45)
    
    mostrar_ayuda()
    
    respuesta = input().lower().strip()
    
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        organizar_archivos()
        input("\nPresiona ENTER para cerrar...")
    else:
        print("Operación cancelada.")
