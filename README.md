Laboratorio 4 de Sistemas Inteligentes - Detección de bordes y API

## Descripción
En este proyecto se desarrollo una API en Python usando FastAPI y OpenCV.

La API permite subir una imagen, procesarla y detectar bordes. Como resultado devuelve un JSON con:

- alto de la imagen
- ancho de la imagen
- si se detectaron bordes

## Estructura básica
- `src/lab4_api_cv/api/main.py`: API principal
- `src/lab4_api_cv/services/image_service.py`: procesamiento de imagen
- `tests/test_api.py`: prueba basica
