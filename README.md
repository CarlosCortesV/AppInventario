# Simulación de Arquitectura Multinivel en Python

Este proyecto simula una aplicación con arquitectura multinivel utilizando Python. Consta de tres componentes principales: un cliente frontend, un servidor backend y una base de datos. La aplicación permite a los usuarios enviar solicitudes para consultar y actualizar datos, demostrando una estructura básica de aplicación distribuida.

## Estructura del Proyecto

![image](https://github.com/user-attachments/assets/7d1f3991-3df9-49cd-b652-050b48dd9493)

## Componentes

### Frontend
El frontend está implementado en client.py, que se encarga de recibir la entrada del usuario y enviar solicitudes al servidor backend. Muestra las respuestas del servidor, permitiendo a los usuarios interactuar con la aplicación.

### Backend
El backend está implementado en server.py, que configura un servidor web para escuchar solicitudes entrantes. Redirige las solicitudes al manejador adecuado según el tipo de solicitud. Los manejadores se encuentran en el directorio `handlers`:
- `data_query_handler.py`: Procesa las solicitudes de consulta y recupera información de la base de datos.
- `data_update_handler.py`: Procesa las solicitudes de actualización y modifica la base de datos según sea necesario.

### Base de Datos
- El motor de base datos empleado para este proyecto en MySQL.
- La bd se llama inventory_db
- Usuario: root
- Contraseña: carlos12
- Y se empleo `import mysql.connector`

## Setup Instructions

1. Clona el repositorio:
   ```
   git clone <repository-url>
   cd multi_level_architecture
   ```

2. Instala las dependencias requeridas:
   ```
   pip install -r requirements.txt
   ```

3. Ejecuta el servidor backend:
   ```
   python web_frontend\app.py
   ```

4. En una terminal separada, ejecuta el cliente frontend:
   ```
   python server.py
   ```

## Ejemplos de Uso

- Para consultar datos, sigue las indicaciones en el cliente frontend para enviar una solicitud al backend.
- Para actualizar datos, proporciona la información necesaria según las indicaciones del cliente frontend.

## Visión General de la Arquitectura
Este proyecto demuestra una arquitectura simple de múltiples niveles, donde el frontend se comunica con el backend, y este a su vez interactúa con la base de datos. Esta separación de responsabilidades permite una mejor organización y escalabilidad de la aplicación.
