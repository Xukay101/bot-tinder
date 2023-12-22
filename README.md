# BotTinder

## Tabla de Contenidos

- [Descripcion del Repositorio](#descripcion-del-repositorio)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Configuracion Inicial](#configuracion-inicial)
- [Credenciales y Configuración](#credenciales-y-configuración)
- [Resolución de XPaths](#resolución-de-xpaths)

## Descripcion del Repositorio

Este repositorio contiene un bot de Tinder desarrollado con Selenium, diseñado para automatizar el sistema de likes. El bot utiliza Python y está diseñado específicamente para Linux.

## Estructura del Proyecto

- **src**: Directorio principal del bot Tinder.
  - **bot.py**: Lógica principal del bot.
  - **config.py**: Archivo de configuración principal.
  - **logger_config.py**: Configuración del registro de eventos.
  - **main.py**: Punto de entrada principal de la aplicación.
  - **utils.py**: Utilidades y funciones auxiliares.

- **bot.log**: Registro de eventos del bot.
- **README.md**: Documentación principal del proyecto.
- **requirements.txt**: Lista de dependencias del proyecto.

## Configuracion Inicial

1. Clona este repositorio:
```bash
git clone https://github.com/Xukay101/bot-tinder
cd bot-tinder
```
2. Instala las dependencias (Previamente se recomienda instalar un entorno virtual):
```bash
pip install -r requirements.txt
```
3. Configura el archivo config.py en el directorio src con tu información de cuenta y preferencias. Si se esta utilizando en un sistema windows sera necesario modificar el `DRIVER_PATH` hacia donde se encuentre.
Para descargar el driver entrar en [link](https://googlechromelabs.github.io/chrome-for-testing/)
4. Ejecuta el bot:
```bash
python src/main.py
```

## Credenciales y Configuración

Se guardan las credenciales de cuenta de Google y contraseña de Google en un archivo .env en el directorio raíz del proyecto. Debes seguir el formato del archivo .env.example.
```bash
cp .env.example .env
```

## Resolución de XPaths

Para obtener XPaths específicos de Tinder, inspecciona los elementos de la página web usando las herramientas de desarrollo del navegador y actualiza el archivo config.py en consecuencia.
