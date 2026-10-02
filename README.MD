# Llama Intent Classifier

Sistema de clasificación de intenciones basado en **Llama**, utilizando fine-tuning para identificar automáticamente el propósito de los mensajes recibidos.

El proyecto implementa un flujo completo que parte de la generación del dataset, continúa con el entrenamiento y validación del modelo, fusiona los adaptadores con el modelo base, prepara el modelo para **Ollama** y finalmente expone el servicio mediante **ngrok**.

## Flujo del proyecto

```text
                 ┌──────────────────────────┐
                 │ genera_train_validation.py│
                 └────────────┬─────────────┘
                              │
                              ▼
                    train.jsonl
                  validation.jsonl
                              │
                              ▼
                 ┌──────────────────────────┐
                 │     fine_tuning.py       │
                 └────────────┬─────────────┘
                              │
                              ▼
                      Modelo LoRA
                              │
                              ▼
                 ┌──────────────────────────┐
                 │        prueba.py         │
                 └────────────┬─────────────┘
                              │
                         Validación
                              │
                              ▼
                 ┌──────────────────────────┐
                 │         fusion.py        │
                 └────────────┬─────────────┘
                              │
                              ▼
                    Modelo fusionado
                              │
                              ▼
                           Ollama
                              │
                              ▼
                 ┌──────────────────────────┐
                 │    prueba_ollama.py      │
                 └────────────┬─────────────┘
                              │
                         Validación
                              │
                              ▼
                 ┌──────────────────────────┐
                 │   ngrok_tunel_api.py     │
                 └────────────┬─────────────┘
                              │
                              ▼
                     API pública HTTPS
```

---

## Objetivo

El modelo clasifica cada mensaje en una de las siguientes intenciones:

| Intención      | Descripción                                                            |
| -------------- | ---------------------------------------------------------------------- |
| `AGENDAR_MEET` | El usuario quiere agendar o coordinar una llamada o videollamada.      |
| `SOLICITAR_CV` | El usuario quiere recibir, consultar o descargar el CV.                |
| `OTRA`         | Cualquier mensaje que no corresponda a las dos intenciones anteriores. |

El modelo está configurado para responder únicamente con la etiqueta correspondiente.

---

# Estructura del proyecto

```text
D:\Asistente
│
├── llama-intent/                 # Checkpoints / adaptadores del fine-tuning
├── llama-intent-merged/          # Modelo fusionado con el modelo base
├── llama-gguf/                   # Modelo convertido para GGUF
├── llama.cpp/                    # Código fuente de llama.cpp
│
├── fine_tuning.py                # Fine-tuning del modelo
├── fusion.py                     # Fusiona LoRA con el modelo base
├── genera_train_validation.py    # Genera los datasets
├── prueba.py                     # Pruebas directas del modelo
├── prueba_ollama.py              # Pruebas utilizando Ollama
├── ngrok_tunel_api.py            # Levanta la API y crea el túnel ngrok
│
├── train.jsonl                   # Dataset de entrenamiento
├── validation.jsonl              # Dataset de validación
│
└── .env                          # Variables de entorno y credenciales
```

> Los directorios que contienen modelos y credenciales deben mantenerse fuera del control de versiones.

---

# Pipeline de entrenamiento

## 1. Generación del dataset

El proceso comienza con:

```bash
python genera_train_validation.py
```

Este script genera los datasets utilizados durante el entrenamiento y validación:

```text
train.jsonl
validation.jsonl
```

El dataset contiene ejemplos de conversaciones/mensajes asociados a una de las tres intenciones:

```text
AGENDAR_MEET
SOLICITAR_CV
OTRA
```

Los archivos `.jsonl` constituyen la entrada para el proceso de fine-tuning.

---

## 2. Fine-tuning

Una vez generados los datasets, se ejecuta:

```bash
python fine_tuning.py
```

Este proceso realiza el fine-tuning del modelo utilizando **LoRA**, permitiendo entrenar una pequeña cantidad de parámetros adicionales en lugar de modificar directamente todos los pesos del modelo base.

Como resultado se generan los checkpoints/adaptadores del modelo entrenado.

La estructura puede contener diferentes checkpoints, por ejemplo:

```text
llama-intent/
├── checkpoint-132/
├── checkpoint-264/
└── checkpoint-396/
```

La selección del checkpoint puede realizarse posteriormente mediante las pruebas del modelo.

---

# 3. Pruebas del modelo

Después del entrenamiento se utiliza:

```bash
python prueba.py
```

Este script permite comprobar directamente el comportamiento del modelo antes de integrarlo con Ollama.

La finalidad es verificar que las entradas produzcan las mismas categorías esperadas:

```text
Mensaje
   │
   ▼
Modelo fine-tuned
   │
   ├── AGENDAR_MEET
   ├── SOLICITAR_CV
   └── OTRA
```

Esta etapa permite detectar problemas en el entrenamiento antes de continuar con la conversión o despliegue.

---

# 4. Fusión del modelo

Una vez validado el modelo fine-tuned, se ejecuta:

```bash
python fusion.py
```

Este proceso combina:

```text
Modelo base
     +
Adaptador LoRA
     │
     ▼
Modelo fusionado
```

El resultado se almacena en:

```text
llama-intent-merged/
```

El propósito de esta etapa es obtener un modelo independiente del adaptador LoRA, facilitando posteriormente su conversión y carga en otras herramientas.

---

# 5. Preparación para Ollama

Después de obtener el modelo fusionado, se prepara el modelo para ejecutarlo mediante **Ollama**.

Dependiendo del formato utilizado, el modelo puede convertirse a **GGUF** y almacenarse en:

```text
llama-gguf/
```

Posteriormente se crea la configuración correspondiente de Ollama utilizando un `Modelfile`.

Un ejemplo de configuración conceptual es:

```text
FROM <modelo>

SYSTEM """
Clasifica el mensaje del usuario en exactamente una de estas intenciones:
AGENDAR_MEET, SOLICITAR_CV u OTRA.

Responde únicamente con la etiqueta.
"""

PARAMETER temperature 0
PARAMETER num_predict 10
```

El modelo puede registrarse posteriormente en Ollama con:

```bash
ollama create llama-intent -f Modelfile
```

Y ejecutarse mediante:

```bash
ollama run llama-intent
```

---

# 6. Pruebas utilizando Ollama

Una vez que el modelo se encuentra disponible en Ollama, se ejecuta:

```bash
python prueba_ollama.py
```

El objetivo es comprobar que el comportamiento del modelo mediante Ollama sea equivalente al comportamiento observado durante las pruebas directas.

El flujo en esta etapa es:

```text
Mensaje
   │
   ▼
API / Ollama
   │
   ▼
Modelo Llama
   │
   ▼
AGENDAR_MEET
SOLICITAR_CV
OTRA
```

Esto permite validar el modelo dentro del entorno en el que será utilizado realmente.

---

# 7. Exposición del servicio mediante ngrok

Finalmente se levanta el servicio con:

```bash
python ngrok_tunel_api.py
```

Este script inicia la API local y establece un túnel mediante **ngrok**, permitiendo acceder al servicio desde Internet.

El flujo final queda:

```text
Cliente
   │
   ▼
Endpoint HTTPS de ngrok
   │
   ▼
API local
   │
   ▼
Ollama
   │
   ▼
Modelo Llama
   │
   ▼
Intención detectada
```

Esto permite integrar el modelo con aplicaciones externas, servicios web o plataformas que necesiten enviar mensajes al clasificador.

---

# Requisitos

Se requiere tener instalado:

* Python
* Ollama
* ngrok
* Dependencias necesarias para el entrenamiento
* Dependencias necesarias para ejecutar la API

Se recomienda utilizar un entorno virtual de Python:

```powershell
python -m venv .venv
```

Activación en Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Posteriormente instalar las dependencias:

```powershell
pip install -r requirements.txt
```

> El archivo `requirements.txt` debe contener las versiones de las librerías utilizadas por el proyecto.

---

# Variables de entorno

Las credenciales y configuraciones sensibles se almacenan en:

```text
.env
```

Este archivo **no debe subirse al repositorio**.

Ejemplo:

```env
NGROK_AUTHTOKEN=xxxxxxxxxxxxxxxx
VERIFY_TOKEN=xxxxxxxxxxxxxxxx
```

Para compartir el proyecto, se recomienda crear un archivo:

```text
.env.example
```

con únicamente los nombres de las variables:

```env
NGROK_AUTHTOKEN=
VERIFY_TOKEN=
```

---

# Ejecución completa

El proceso completo puede resumirse en los siguientes pasos:

### 1. Generar dataset

```powershell
python genera_train_validation.py
```

### 2. Entrenar el modelo

```powershell
python fine_tuning.py
```

### 3. Probar el modelo

```powershell
python prueba.py
```

### 4. Fusionar el modelo

```powershell
python fusion.py
```

### 5. Convertir/preparar el modelo para Ollama

Generar el modelo en formato compatible y configurar el `Modelfile`.

### 6. Cargar el modelo en Ollama

```powershell
ollama create llama-intent -f Modelfile
```

### 7. Verificar Ollama

```powershell
python prueba_ollama.py
```

### 8. Levantar la API y el túnel

```powershell
python ngrok_tunel_api.py
```

---

# Arquitectura final

El sistema completo puede verse como cuatro etapas:

```text
┌─────────────────────┐
│      DATASET        │
│                     │
│ train.jsonl         │
│ validation.jsonl    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       TRAINING      │
│                     │
│ fine_tuning.py      │
│ LoRA                │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     MODEL BUILD     │
│                     │
│ prueba.py           │
│ fusion.py           │
│ GGUF / Ollama       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      DEPLOYMENT     │
│                     │
│ Ollama              │
│ prueba_ollama.py    │
│ ngrok_tunel_api.py  │
└─────────────────────┘
```

---

# Filosofía del proyecto

El proyecto separa claramente las diferentes responsabilidades del ciclo de vida del modelo:

**Generación de datos → Entrenamiento → Validación → Fusión → Ejecución local → Exposición como API**

Esta separación facilita modificar cada etapa de manera independiente, repetir el entrenamiento y validar el modelo antes de ponerlo en producción.

---

# Estado actual

El proyecto está orientado a un clasificador ligero de intenciones para integrarse posteriormente con un sistema de atención/conversación automatizada.

Las intenciones actuales son:

```text
AGENDAR_MEET
SOLICITAR_CV
OTRA
```

La intención `OTRA` permite identificar mensajes que no requieren una de las acciones específicas y deja abierta la posibilidad de implementar posteriormente un flujo conversacional independiente para este tipo de mensajes.
