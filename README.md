# Traductor de Señaz - Uso de Api de VoiceFlow

Este proyecto muestra cómo usar las APIs de Voiceflow para crear un chatbot para sugerencia, registrar y atender a usuario no oyente. Puedes chatear directamente con tu agente de Voiceflow desde la consola.

## Cómo empezar (3 pasos simples)

### Lo que necesitas:
- Python instalado en tu computadora
- Una cuenta de Voiceflow con un proyecto publicado
- Tu clave API de Voiceflow

### Instalación rápida:

**1. Instalar dependencias**
```bash
cd LAB10
pip install requests
```

**2. Configurar tu API**
- Abre el archivo `VoiceflowAPIGuide.py`
- En las líneas 2-4, cambia estos valores por los tuyos:
```python
api_key = 'TU_API_KEY_AQUI'
projectID = "TU_PROJECT_ID_AQUI"  
versionID = "TU_VERSION_ID_AQUI"
```

**3. Ejecutar**
```bash
python VoiceflowAPIGuide.py
```

## Archivos del proyecto

```
LAB10/
├── VoiceflowAPIGuide.py     # Archivo principal (ESTE ES EL QUE USAS)
├── requirements.txt         # Dependencias de Python
└── README.md               # Esta guía
```

## Como obtener tus claves de Voiceflow

### Obtener tu API Key (Obligatorio)
1. Ve a tu proyecto en Voiceflow
2. Haz clic en **Settings** (Configuración)
3. Ve a **API Keys** 
4. Copia tu **Primary Key** (empieza con `VF.DM.`)

### Obtener Project ID y Version ID (Para guardar conversaciones)
**Project ID:**
1. En **Settings** → **General**
2. Copia el **Project ID**

**Version ID:**
1. Ve a la pestaña **Versions** 
2. Copia el ID completo de tu versión publicada

### Configurar en tu archivo
Edita estas líneas en `VoiceflowAPIGuide.py`:
```python
api_key = 'VF.DM.TU_CLAVE_AQUI'        # Obligatorio
projectID = "tu_project_id_aqui"        # Para transcripts  
versionID = "tu_version_id_aqui"        # Para transcripts
```

## Qué hace este programa

- **Chatear con tu agente**: Habla con tu bot de Voiceflow desde la consola
- **Botones interactivos**: Cuando aparezcan opciones, elige un número
- **Guardar conversaciones**: Las conversaciones se guardan automáticamente
- **Manejo de errores**: Te avisa si algo no funciona

## Como usar el programa

### Comandos básicos:
- **Escribe cualquier mensaje** para hablar con tu bot
- **Escribe un número (1, 2, 3...)** cuando aparezcan botones  
- **Escribe 'quit', 'exit' o 'bye'** para salir
- **Presiona Ctrl+C** para cerrar forzadamente

### Ejemplo de conversación:

```
Voiceflow API Guide - Python Implementation
==================================================

> What is your name? Juan

Starting conversation for user: Juan
------------------------------
Hola Juan! ¿En qué puedo ayudarte hoy?

Choose one of the following:
  1. Información sobre productos
  2. Soporte técnico  
  3. Hablar con un humano

> Choose a button number, or type a reply: 1
Great choice! Here are our products...

> Say something: Gracias
De nada! ¿Algo más?

> Say something: quit
The conversation has ended.
```

## Solución de problemas

### Errores comunes y soluciones:

**"Error making request to Voiceflow API"**
- Verifica que tu API key sea correcta
- Asegúrate que tu proyecto esté PUBLICADO en Voiceflow
- Revisa tu conexión a internet

**"Error: Please set your Voiceflow API key"**  
- Tu API key no está configurada
- Debe empezar con `VF.DM.`
- Cópiala completa desde Voiceflow

**"Failed to save transcript"**
- Project ID y Version ID no están configurados
- Usa el ID completo de la versión, no solo "production"

## Pasos para hacer funcionar tu bot

### 1. Preparar tu proyecto en Voiceflow
- Crea un bot en Voiceflow
- **IMPORTANTE:** Haz clic en **PUBLISH** (publicar) para que funcione
- Ve a Settings > API Keys y copia tu clave

### 2. Configurar el código
```python
# Edita estas 3 líneas en VoiceflowAPIGuide.py:
api_key = 'VF.DM.tu_clave_real_aqui'
projectID = "tu_project_id_aqui" 
versionID = "tu_version_id_aqui"
```

### 3. Ejecutar  
```bash
cd LAB10
pip install requests
python VoiceflowAPIGuide.py
```

## Comandos útiles

**Para probar si funciona:**
```bash
python test_setup.py
```

**Para usar el bot:**
```bash
python VoiceflowAPIGuide.py
```

## Recursos útiles

- **Documentación de Voiceflow:** [developer.voiceflow.com](https://developer.voiceflow.com)
- **Librería requests de Python:** [docs.python-requests.org](https://docs.python-requests.org)

## Notas importantes

- Tu proyecto de Voiceflow **DEBE** estar publicado
- El API key empieza con `VF.DM.`
- Si no configuras Project ID y Version ID, no se guardarán las conversaciones (pero el chat funcionará)

---

**¡A chatear con tu bot!**

*Esta guía te enseña cómo conectar Python con Voiceflow de forma simple.*
