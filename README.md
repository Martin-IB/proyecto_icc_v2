# Sistema Web de Monitoreo con Inteligencia Artificial

Este proyecto consiste en un sistema web de monitoreo que permite a los usuarios visualizar datos de sensores en tiempo real y realizar consultas por voz utilizando inteligencia artificial. El sistema está desarrollado con un backend en FastAPI, un frontend en React, y se despliega en la nube mediante Docker Compose sobre una instancia EC2 de AWS.

El backend implementa una API RESTful desarrollada en FastAPI que se encarga de recibir, procesar y exponer los datos provenientes de sensores. También incluye funcionalidades de inteligencia artificial como el reconocimiento de voz a través de la Web Speech API. La base de datos utilizada es PostgreSQL, contenedorizada para facilitar su integración y despliegue.

El frontend, desarrollado en React, permite a los usuarios visualizar gráficas en tiempo real, acceder a registros históricos y controlar la interacción mediante comandos de voz como “iniciar monitoreo” o “consultar temperatura”, mejorando la experiencia del usuario en entornos experimentales.

La apliccacion está dockerizado mediante Docker Compose, garantizando la portabilidad y consistencia del entorno de desarrollo y producción. Cada componente (backend, frontend y base de datos) corre en un contenedor independiente, permitiendo una arquitectura desacoplada y escalable.

El despliegue se realiza en la nube utilizando una instancia EC2 de AWS. La instancia se configura con Docker y Docker Compose para lanzar la aplicación, exponiendo los servicios a través del puerto 80 con un servidor Nginx, lo que permite el acceso público a la aplicación web desde cualquier navegador.

## Requisitos previos

- Cuenta en AWS
- Docker y Docker Compose instalados
- Clave SSH para acceso a la instancia EC2

## Despliegue

1. Crear una instancia EC2 en AWS con Ubuntu.
2. Configurar el grupo de seguridad para permitir el tráfico HTTP (puerto 80), SSH (puerto 22), puerto 8000 y 3000.
3. Conectarse a la instancia vía SSH.
4. Clonar el repositorio en la instancia EC2.
5. Hacer sudo git clone https://github.com/Martin-IB/proyecto_icc_v2.git
6. Instalar Docker y Docker Compose.
7. Ejecutar `docker-compose up -d` en la carpeta del proyecto.
8. Acceder a la aplicación desde el navegador usando la IP pública de la instancia EC2.
9. Acceder al backend mediante http://3.132.200.37:8000
10. Acceder al frontend mediante http://3.132.200.37:8000

